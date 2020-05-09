import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/chmaquina")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src")
import falcon
from runTest import test
class QuoteResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': test()
            # 'author': self.test()
        }
        resp.media = quote
    
    # def test(self):
    #     return "hello"



api = falcon.API()
api.add_route('/quote', QuoteResource())