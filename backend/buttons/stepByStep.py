import falcon, json

class MachinaStep(object):

    def __init__(self, ch):
        self.ch              = ch
        self.instructions    = None
        self.numPrograms     = None
        self.algorithm       = None
    
    def on_post(self, req, resp):

        data = raw_data = json.load(req.bounded_stream)
        self.algorithm = raw_data.get('algorithm')
        print(f"algorithm: {self.algorithm}")
        resp.status = falcon.HTTP_200
        
        if self.instructions == None:
            self.instructions = self.ch.getPrograms()
            self.numPrograms  = len(self.instructions)
            print("instructions", self.instructions, "\n\n")

        if len(self.instructions) == 0:
            self.instructions = None
            return

        if self.algorithm == None:
            return 
        self.ch.run_line(self.algorithm)
        resp.status = falcon.HTTP_201


    def on_get(self, req, resp):
        dispatcher = self.ch.dispatcher
        data = {
            'acumulador': self.ch.getAcumulador(),
            'variables': self.ch.getVariables(),
            'tags': self.ch.getTags(),
            'programs': self.ch.getPrograms(),
            'registers': self.ch.getRegisters(),
            'memory': self.ch.getMemory(),
            'memoryAvailable': self.ch.getMemoryAvailable(),
            'memoryUsed': self.ch.getMemoryUsed(),
            'steps': self.ch.getSteps(), #!
            'stdout': self.ch.getStdout(), #!
            'printer': self.ch.getPrinter(),
        }
        resp.media = data;
        resp.status = falcon.HTTP_201