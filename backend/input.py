import falcon, json

class MachinaInput(object):

    def __init__(self, ch):
        self.ch        = ch
        self.lea_value = None
    
    def on_post(self, req, resp):
        raw_data = json.load(req.bounded_stream)
        self.lea_value = raw_data.get('lea')
        print(self.lea_value)
        resp.status = falcon.HTTP_200


    def on_get(self, req, resp):
        lea  = self.lea_value
        data = {
            'lea': lea,
        }
        if self.lea_value == None:
            resp.media  = data;
            resp.status = falcon.HTTP_200
        else:
            resp.media  = data;
            resp.status = falcon.HTTP_200
            # self.lea_value = None
