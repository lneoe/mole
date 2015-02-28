# coding:utf-8

import tornado.web
from jinja2 import (Environment,
                    FileSystemLoader)


class Application(tornado.web.Application):

    """
    Custom Application from tornado.web.Application
    register custom attributes and function
    """

    def __init__(self, *args, **kwargs):
        """
        registed jinja templates engine
        """
        templates_path = kwargs.get("templates_path", "templates")
        settings = dict(
            jinja=Environment(loader=FileSystemLoader(templates_path)),
        )
        kwargs.update(settings)

        super(Application, self).__init__(*args, **kwargs)
