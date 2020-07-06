import os, sys
import falcon, json


class MachinaRunner(object):

    def __init__(self, ch):
        self.ch = ch
        self.algorithm = None

    def on_get(self, req, resp):
        if self.algorithm == None:
            return
        self.ch.run_all(self.algorithm) 
        print("in runner stdout", self.ch.getStdout())
        print("in acumulador ", self.ch.getAcumulador())
        data = {
            'stdout':  self.ch.getStdout(),
            'printer': self.ch.getPrinter(),
            'acumulador': self.ch.getAcumulador(),
            'steps':   self.ch.getSteps(),
            'memory':  self.ch.getMemory(),
        }
        resp.media = data;
        resp.status = falcon.HTTP_201

    def on_post(self, req, resp):
        data = raw_data = json.load(req.bounded_stream)
        self.algorithm = raw_data.get('algorithm')
        resp.status = falcon.HTTP_200

