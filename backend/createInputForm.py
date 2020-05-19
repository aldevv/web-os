import falcon, json

class MachinaInputCreate(object):

    def __init__(self, ch):
        self.ch       = ch
        self.createForm = False
    
    #maquina sends signal to see if there is a lea command called
    def on_post(self, req, resp):
        """
        https://github.com/yohanboniface/falcon-multipart
        """
        raw_data = json.load(req.bounded_stream)
        self.createForm = raw_data.get('createForm')
        resp.status = falcon.HTTP_200

    #front uses this to create the form if createForm is true
    def on_get(self, req, resp):
        createForm  = self.createForm
        data = {
            'createForm': createForm,
        }
        if self.createForm == False:
            resp.media  = data;
            resp.status = falcon.HTTP_200
        else:
            resp.media  = data;
            resp.status = falcon.HTTP_200
            # self.createForm = False
