import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/chmaquina")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src")
import falcon
from chmaquina import Chmaquina


class QuoteResource:

    def __init__(self):
        self.ch = Chmaquina()
        self.ch.compileFile('programs/factorial.ch')
        self.ch.run_all()

    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'acumulador': self.ch.getAcumulador(),
            'variables': self.ch.getVariables(),
            'tags': self.ch.getTags(),
            'memory': self.ch.getMemory(),
            'stdout': self.ch.getStdin(),
            # 'variables': (
            # ),
            # 'author': self.test()
        }
        resp.media = quote
    
    # def test(self):
    #     return "hello"



api = falcon.API()
api.add_route('/quote', QuoteResource())