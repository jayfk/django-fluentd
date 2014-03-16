import logging

from django.views.generic import TemplateView

logger = logging.getLogger("django")

class IndexView(TemplateView):

    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        #print "foo"
        #logging.debug("debug message")
        #logging.info("info message")
        #logging.warning("warning message")
        #logging.error("error message")
        #logging.critical("fatal message")
        foo = 1/0
        return super(IndexView, self).dispatch(request, *args, **kwargs)