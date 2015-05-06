# coding:utf-8

import logging
import hashlib

from .utils import verify_password


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
