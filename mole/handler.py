# coding:utf-8

import logging
import uuid
import tornado.web
from tornado.escape import json_encode

from .database import before_request_handler as db_connect
from .database import after_request_handler as db_close
from .session import Session


class BaseRequestHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        # self._session = self.settings.get("session")
        self._session = Session(self.settings.get("session_store"))
        self.jinja.globals.update(self.get_template_namespace())

    def initialize(self):
        logging.debug("Connect database on handler initialize")
        db_connect()

    def on_finish(self):
        logging.debug("Close database connection on handler finish!")
        db_close()

    # def prepare(self):
    #     self.get_or_create_sessionid()

    def get_or_create_sessionid(self):
        """
        get sessionid if not exist create it
        """
        logging.debug("Try to get SessionID")
        sessionid = self.get_secure_cookie("sessionid")

        if not sessionid:
            sessionid = uuid.uuid1().hex
            logging.debug("SessionID not exist create one:[{0}]"
                          .format(sessionid))
            self.set_secure_cookie("sessionid", sessionid)

        logging.debug("The SessionID was:[{0}]".format(sessionid))
        return sessionid

    @property
    def session(self):
        sessionid = self.get_or_create_sessionid()
        # sessionid = self.get_secure_cookie("sessionid")
        self._session.load(sessionid)
        return self._session

    @property
    def jinja(self):
        """
        use jinja as property
        """
        return self.settings.get("jinja")

    # @jinja.setter
    # def jinja(self, value):
    #     self.settings["jinja"] = value

    # def get_current_user(self):
    #     user = self.get_secure_cookie("sessionid")
    #     return user

    def response_json(self, json_str):
        return self.render_json(json_str)

    def render_json(self, json_str):
        """
        render and response json message with given str or iterable dict
        """
        self.set_header('Content-Type', 'application/json')

        settings = self.application.settings
        if settings.get("xsrf_cookies", False):
            self.xsrf_form_html()

        if not isinstance(json_str, str):
            json_str = json_encode(json_str)
        self.finish(json_str)

    def render_string(self, template_name, **context):
        """
        jinja render template
        """
        template = self.jinja.get_template(template_name)
        return template.render(**context)

    def render_from_string(self, template_string, **context):
        """
        jinja render html with given string
        """
        template = self.jinja.from_string(template_string)
        return template.render(**context)

    def render(self, template_name, **context):
        """
        render template with given context
        """
        settings = self.application.settings
        if settings.get("xsrf_cookies", False):
            self.xsrf_form_html()
        html = self.render_string(template_name, **context)
        self.finish(html)
