import os, sys
import falcon


class MachinaRunner(object):

    def __init__(self, ch):
        self.ch = ch

    def on_get(self, req, resp):
        self.ch.run_all() 
        print("in runner stdout", self.ch.getStdout())
        data = {
            'stdout': self.ch.getStdout(),
            'printer': self.ch.getPrinter(),
            'steps': self.ch.getSteps(),
            'memory': self.ch.getMemory(),
        }
        resp.media = data;
        resp.status = falcon.HTTP_201
