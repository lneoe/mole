# coding: utf-8

from wtforms import Form as WTForm
from wtforms import StringField
from wtforms.widgets import Input as InputWidget
from tornado import locale


class TornadoInputWrapper(object):

    def __init__(self, mulitdict):
        self._wrapped = dict()
        for key, values in mulitdict.items():
            # if isinstance(values, list) or isinstance(values, tuple):
            for value in values:
                self._wrapped[key] = [
                    value.decode('utf-8') if isinstance(value, bytes)
                    else value]

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def __contains__(self, name):
        return (name in self._wrapped)

    def __getitem__(self, name):
        return self._wrapped[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def getlist(self, name):
        item = self._wrapped[name]
        if isinstance(item, list) or isinstance(item, tuple):
            return self._wrapped[name]
        else:
            return [self._wrapped[name]]


class Form(WTForm):

    """
    `WTForms` wrapper for Tornado.
    """

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        self._locale_code = kwargs.get("locale", "en_US")
        super(Form, self).__init__(formdata, obj, prefix, **kwargs)

    def _get_translations(self):
        return TornadoLocaleWrapper(self._locale_code)

    def process(self, formdata=None, obj=None, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoInputWrapper(formdata)
        super(Form, self).process(formdata, obj, **kwargs)


class TornadoLocaleWrapper(object):

    def __init__(self, code):
        self.locale = locale.get(code)

    def gettext(self, message):
        return self.locale.translate(message)

    def ngettext(self, message, plural_message, count):
        return self.locale.translate(message, plural_message, count)


class EmailWidget(InputWidget):
    input_type = "email"


class EmailField(StringField):
    widget = EmailWidget()
