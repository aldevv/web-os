import falcon, json

class MachinaInput(object):

    def __init__(self, ch):
        self.ch        = ch
        self.lea_value = []
    
    def on_post(self, req, resp):
        raw_data = json.load(req.bounded_stream)
        self.lea_value.append(raw_data.get('lea'))
        print(self.lea_value)
        resp.status = falcon.HTTP_200


    def on_get(self, req, resp):
        if self.lea_value == []:
            resp.media  = None
            return
        lea  = self.lea_value.copy()
        data = {
            'lea': lea,
        }
        resp.media  = data
        self.lea_value = []
        resp.status = falcon.HTTP_200
