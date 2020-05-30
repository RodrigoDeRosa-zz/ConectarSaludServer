from datetime import timedelta

from tornado.ioloop import IOLoop


class Scheduler:

    @classmethod
    def run_in_millis(cls, coroutine, millis=0):
        """ Set coroutine to run given milliseconds from now. """
        IOLoop.current().add_timeout(timedelta(milliseconds=millis), coroutine)
