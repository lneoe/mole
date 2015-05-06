# coding:utf-8

import os
import sys
# import uuid
# import hashlib
# import base64
import datetime
import time

from passlib.hash import pbkdf2_sha256


def encrypt_password(password):
    try:
        update_time = datetime.datetime.utcnow().timestamp()
    except Exception:
        update_time = time.mktime(time.gmtime())

    secret = pbkdf2_sha256.encrypt(password)
    return secret + '$$' + str(update_time)


def verify_password(raw_password, hashed):
    _hash, update_time = hashed.split("$$")
    return pbkdf2_sha256.verify(raw_password, _hash)


def set_password(user, password_hash, commit=True):
    user.update(password=password_hash)
    if commit:
        user.save()
    return user


def find_subclass(cls):
    sub_class = cls.__subclasses__()
    return sub_class


def find_modelclass(ModelClass):
    proj_path = sys.path[0]
    model_path = os.path.join(proj_path, "models")

    model_class = [s.split(".")[0] for s in os.listdir(model_path)
                   if not s.startswith("__") and s.endswith("py")]
    for m in model_class:
        __import__("models." + m)

    sub_class = ModelClass.__subclasses__()
    return sub_class


if __name__ == "__main__":
    _hash = encrypt_password("c4ca4238a0b923820dcc509a6f75849b")
    print(_hash)
    print(verify_password("c4ca4238a0b923820dcc509a6f75849b", _hash))
