# coding:utf-8

import os
import sys
import uuid
import hashlib
import base64
import datetime
import time


def encrypt_password(password):
    salt = uuid.uuid4().bytes
    try:
        update_time = datetime.datetime.utcnow().timestamp()
    except Exception:
        update_time = time.mktime(time.gmtime())

    update_time = str(update_time)
    password = str(password)

    # python2 python3 complex
    try:
        password_bytes = bytes(password)
        update_time = bytes(update_time)
    except TypeError:
        password_bytes = bytes(password, "utf-8")
        update_time = bytes(update_time, "utf-8")

    pw_salt = password_bytes + salt
    hash_pw = hashlib.sha1(pw_salt).digest()

    # not realy need for b64encode
    secret = base64.b64encode(hash_pw + b'|' + salt + b"|" + update_time)

    return secret


def decrypt_password(secret):
    pw_salt, salt, update_time = base64.b64decode(secret).split(b'|')
    return pw_salt, salt, update_time


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
    model_path = os.path.join(proj_path, "model")

    model_class = [s.split(".")[0] for s in os.listdir(model_path)
                   if not s.startswith("__") and s.endswith("py")]
    for m in model_class:
        __import__("model." + m)

    sub_class = ModelClass.__subclasses__()
    return sub_class


if __name__ == "__main__":
    print(encrypt_password(1))
