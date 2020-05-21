import falcon, json

class MachinaClean(object):

    def __init__(self, ch):
        self.ch        = ch
    
    def on_post(self, req, resp):
        raw_data = json.load(req.bounded_stream)
        print(raw_data)
        self.ch.clean(int(raw_data.get('memoria')), int(raw_data.get('kernel')), int(raw_data.get('acumulador')))
        resp.status = falcon.HTTP_200