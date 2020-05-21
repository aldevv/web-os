
class FileInfo:
    def __init__(self, mem):
        self.mem = mem
        self.filenames = []
        self.declarationHistory = {}

    def getVariables(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getVariables())
        return all_

    def getTags(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getTags())
        return all_

    def saveDeclaration(self, declaration, update=None):
        if update == True:
            last_element = len(self.declarationHistory) - 1
            self.declarationHistory[last_element] = declaration
        else:
            self.declarationHistory[len(self.declarationHistory)] = declaration

    def getRegisters(self):
        files = self.getFilenames()
        ins   = self.getProgramsLength()
        rb    = self.getBaseRegisters()
        rlc   = self.getCodeLimitRegisters()
        rlp   = self.getProgramLimitRegisters()
        registers = [files, ins, rb, rlc, rlp]
        return registers

    def getFilenames(self):
        return self.filenames

    def getProgramsLength(self):
        programs = self.mem.programs_saved()
        registers = []
        for program in programs:
            registers.append(len(program))
        return registers
    
    def getBaseRegisters(self):
        base = self.mem.getKernel() + 1
        programs = self.mem.programs_saved()
        registers = []
        registers.append(base)
        if len(programs) > 1: #!
            for i in range(1, len(programs)):
                registers.append( registers[-1] + len(programs[i-1]) + len(self.declarationHistory[i-1].getAllNames())) # minus the last one which is the current one
        return registers

    def getCodeLimitRegisters(self):
        programs = self.mem.programs_saved()
        registers = []
        rb = self.getBaseRegisters()
        for r,program in zip(rb, programs):
            registers.append(r + len(program))
        return registers

    def getProgramLimitRegisters(self):
        registers = []
        rcl = self.getCodeLimitRegisters()
        for r, id_ in zip(rcl, self.declarationHistory):
            registers.append(r + len(self.declarationHistory[id_].getAllNames()))
        return registers
    
    def saveFilename(self, filename):
        self.filenames.append(filename)

    def clear(self):
        self.filenames = []
        self.declarationHistory = {}