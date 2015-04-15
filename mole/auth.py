# coding:utf-8

import logging
import hashlib

from .utils import decrypt_password


def login(request, user, password, expires_day=None):
    logging.debug("User [{0}] try to login...".format(user))

    if check_password(user.password, password):
        request.set_secure_cookie("user", user.username)
        logging.debug("User check_password valid, login success.")

        session = request.session
        session.username = user.username
        session.expires_day = expires_day
        session.save(session.sessionid, expires_day)

        return user
    else:
        logging.debug("User check_password invalid, login faild.")
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
        if check_password(user.password, password):
            logging.debug("User check_password success.")
            return user
        else:
            logging.debug("User check_password faild.")
            return None


def check_password(raw_password, password):
    password_hash, salt, update_time = decrypt_password(raw_password)
    logging.debug("User has secret password string: {0}".format(password_hash))

    try:
        password = bytes(password)
    except TypeError:
        password = bytes(password, "utf-8")

    _input = hashlib.sha1(password + salt).digest()
    logging.debug("InputPassword hash was: {0}".format(_input))

    return _input == password_hash
