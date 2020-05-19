import os, sys
import falcon


class MachinaRunner(object):

    def __init__(self, ch):
        self.ch = ch

    def on_get(self, req, resp):
        self.ch.run_all()
        data = {
            'stdout': self.ch.getStdout(),
        }
        resp.media = data;
        resp.status = falcon.HTTP_201
