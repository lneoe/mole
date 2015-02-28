# coding: utf-8

import os
import sys
import json

from tornado.util import ObjectDict


def parser_config(file_path=None):
    # proj_path = os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), os.path.pardir))

    proj_path = sys.path[0]
    if not file_path:
        file_path = os.path.join(proj_path, "config.json")
    elif not os.path.isfile(file_path):
        file_path = os.path.join(proj_path, file_path)

    with open(file_path) as fp:
        config = json.load(fp)
        return ObjectDict(config)
