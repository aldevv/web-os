class DataStream:
    def __init__(self):
        self.stdout  = {}
        self.stderr  = {}
        self.printer = {}
    
    def appendStderr(self, declaration, string):
        self.stderr[declaration] = string

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