class DataStream:
    def __init__(self):
        self.stdout  = {}
        self.stderr  = {}
        self.printer = {}
        self.steps   = {}
        self.status  = {} # return value
    
    def appendStderr(self, runner, string):
        self.stderr[runner] = string

    def appendStdout(self, declaration, string):
        if declaration not in self.stdout:
            printer = []
            printer.append(string)
            self.stdout[declaration] = printer
        else:
            self.stdout[declaration].append(string)

    def appendPrinter(self, declaration, string):
        if declaration not in self.printer:
            printer = []
            printer.append(string)
            self.printer[declaration] = printer
        else:
            self.printer[declaration].append(string)

    def getPrinter(self, declaration):
        return self.printer[declaration]

    def getStdout(self, declaration):
        return self.stdout[declaration]
    
    def clearSteps(self):
        self.steps = {}

    def appendStep(self, declaration, string):
        if declaration not in self.steps:
            printer = []
            printer.append(string)
            self.steps[declaration] = printer
        else:
            self.steps[declaration].append(string)

    def getSteps(self, declaration):
        return self.steps[declaration]

    def appendStatus(self, runner, value):
        self.status[runner] = value
    
    def getStatus(self):
        return self.status
    
    def getStderr(self):
        return self.stderr
    
    def appendError(self, runner, error):
        self.stderr[runner] = error