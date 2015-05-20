# coding:utf-8

import logging
import hashlib
import time
import datetime
import hashlib
import hmac

from mole.utils import (verify_password,
                        base36decode,
                        base36encode)


def login(request, user, password, expires_day=None):
    logging.debug("User [{0}] try to login...".format(user))

    if verify_password(password, user.password):
        request.set_secure_cookie("user", user.username)
        logging.debug("User verify_password valid, login success.")

        session = request.session
        session.username = user.username
        session.expires_day = expires_day
        session.save(session.sessionid, expires_day)

        return user
    else:
        logging.debug("User verify_password invalid, login faild.")
        return False


def logout(request):
    logging.debug("User [{0}] try to logout".format(request.current_user))

    session = request.session
    session.clear()
    # request.clear_cookie("sessionid")
    return True


def verify_user(username, password, usermodel):
    try:
        user = usermodel.get(
            (usermodel.username == username) | (usermodel.email == username))
    except usermodel.DoesNotExist:
        logging.debug("User [{0}] does not exist.".format(username))
        return None
    else:
        print(password, user.password)
        if verify_password(password, user.password):
            logging.debug("User check_password success.")
            return user
        else:
            logging.debug("User check_password faild.")
            return None


class PasswordResetTokenGenerator(object):

    def __init__(self, secret='secret'):
        self.secret = str(secret).encode('utf-8')

    def make_token(self, user):
        ts = int(datetime.datetime.today().timestamp())
        # ts_b36 = base36encode(ts)
        return self._make_token(user, ts)

    def check_token(self, user, token):
        ts_b36, _hash = token.split("-")

        ts = base36decode(ts_b36)

        # Todo: more job need, a function like Django's
        # constant_time_compare(val1, val2)
        return token == self._make_token(user, ts)

    def _make_token(self, user, timestamp):
        ts_b36 = base36encode(timestamp)

        key_salt = hashlib.sha1(self.secret).digest()

        value = (str(user.pk) + user.password).encode('utf-8')

        _hash = hmac.new(key=key_salt, msg=value,
                         digestmod=hashlib.sha1).hexdigest()
        return "{0}-{1}".format(ts_b36, _hash)
