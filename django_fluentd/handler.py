from __future__ import print_function

import traceback

from fluent import handler
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class FluentdHandler(handler.FluentHandler):
    """An log handler that sends all incoming logs to a fluentd instance"""

    def __init__(self, *args, **kwargs):
        self.config = self._load_settings()

        super(FluentdHandler, self).__init__(
            tag=self.config["tag"], host=self.config["server"], port=self.config["port"]
        )

    def _load_settings(self):
        """load configuration from settings.py and return a dict"""
        print("loading config")
        config = {
            "server": self._load_settings_option("DJANGO_FLUENTD_SERVER"),
            "port": self._load_settings_option("DJANGO_FLUENTD_PORT"),
            "tag": self._load_settings_option("DJANGO_FLUENTD_TAG")
        }

        return config

    def _load_settings_option(self, var, default=None):
        """loads a variable from djangos settings. If the variable is not defined, and a default value is passed
        over with the call, default value is returned. If no default value is specified, the variable is required
        and a ImproperlyConfigured Exception is raised"""

        try:
            #load and return
            return getattr(settings, var)
        except AttributeError:
            #setting is not defined
            if default is not None:
                print("returning default")
                #but we have a default value that is not None. return it
                return default
            #setting is required but could not be loaded, print to stderr
            raise ImproperlyConfigured("Missing %s in settings. FluentdHandler could not be loaded." % var)

    def has_string_message(self, record):
        """checks if the record has a massage with type str. This is true when the logger is called like this:
         logger.debug("foo")."""
        if isinstance(record.msg, str):
            return True
        return False

    def add_string_to_record(self, record):
        """adds the string in msg.record to a dictionary"""
        record.msg = {"message": record.msg}
        return record

    def has_exception(self, record):
        """returns True if the record has a exc_info"""
        if record.exc_info:
            return True
        return False

    def add_exception_to_record(self, record):
        """adds a traceback (and a message if it is not defined) to record.msg"""
        tb = traceback.format_exception(*record.exc_info)

        if isinstance(record.msg, dict):
            record.msg.update("traceback", tb)
        elif self.has_string_message(record):
            record = self.add_string_to_record(record)
            record.msg.update("traceback", tb)
        else:
            record.msg = {
                "message": record.getMessage(),
                "traceback": tb
            }

        return record

    def emit(self, record):
        #As of fluent-logger v 0.3.3 logged exceptions have no information. Make sure to add a message
        #and to add traceback information if available
        if self.has_exception(record):
            record = self.add_exception_to_record(record)

        #As of fluent-logger v 0.3.3 logs with a plain string as message don't get converted.
        #That's a problem, because logs in the format of logger.debug("foobar") just have no message.
        #convert record.msg to a dict containing the message
        if self.has_string_message(record):
            record = self.add_string_to_record(record)

        return super(FluentdHandler, self).emit(record)