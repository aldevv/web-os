import falcon, json

class MachinaStep(object):

    def __init__(self, ch):
        self.ch           = ch
        self.instructions = None
        self.atStart      = True
    
    def on_post(self, req, resp):
        
        if self.instructions == None:
            input_file = req.get_param('file')
            print("cargué el archivo paso a paso: ", input_file.filename)
            if input_file.filename:
                filename = input_file.filename
                self.instructions = input_file.file.read().decode('utf8').split('\n')
                self.ch.compileLines(self.instructions)
                self.ch.run_line(atStart=True)
                print(self.ch.getStdout())
                return

        if len(self.instructions) == 0:
            self.instructions = None
            return
        print("i ran it") 
        self.ch.run_line()
        print(self.ch.getStdout())
        resp.status = falcon.HTTP_201


    def on_get(self, req, resp):
        if self.ch.instructionRunner != None:
            data = {
                'steps': self.ch.getStdout(),
            }
            resp.media = data;
        else:
            data = {
                'steps': "none"
            }
            resp.media = data;
        resp.status = falcon.HTTP_201