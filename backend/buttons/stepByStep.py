import falcon, json

class MachinaStep(object):

    def __init__(self, ch):
        self.ch           = ch
        self.instructions = None
        self.atStart      = True
    
    def on_post(self, req, resp):
        
        if self.instructions == None:
            self.instructions = self.ch.getPrograms()
            print("instructions", self.instructions)

        if len(self.instructions) == 0:
            self.instructions = None
            return

        self.ch.run_line()
        # print("i ran it") 
        # print("stdout: ", self.ch.getStdout())
        resp.status = falcon.HTTP_201


    def on_get(self, req, resp):
        if self.ch.instructionRunner != None:
            data = {
                'acumulador': self.ch.getAcumulador(),
                'variables': self.ch.getVariables(),
                'tags': self.ch.getTags(),
                'programs': self.ch.getPrograms(),
                'registers': self.ch.getRegisters(),
                'memory': self.ch.getMemory(),
                'memoryAvailable': self.ch.getMemoryAvailable(),
                'memoryUsed': self.ch.getMemoryUsed(),
                'steps': self.ch.getStdout(),
            }
            resp.media = data;
        else:
            data = {
                'steps': "none"
            }
            resp.media = data;
        resp.status = falcon.HTTP_201