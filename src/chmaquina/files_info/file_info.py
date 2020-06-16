
class FileInfo:
    def __init__(self, mem):
        self.mem = mem
        self.filenames = []
        self.filepaths = []

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
        programs = self.mem.get_programs()
        registers = []
        for program in programs:
            registers.append(len(program))
        return registers
    
    def getBaseRegisters(self):
        base = self.mem.getKernel() + 1
        programs = self.mem.get_programs()
        registers = []
        registers.append(base)
        if len(programs) > 1: #!
            for i in range(1, len(programs)):
                registers.append( registers[-1] + len(programs[i-1]) + len(self.mem.getDeclarationHistory()[i-1].getAllNames())) # minus the last one which is the current one
        return registers

    def getCodeLimitRegisters(self):
        programs = self.mem.get_programs()
        registers = []
        rb = self.getBaseRegisters()
        for r,program in zip(rb, programs):
            registers.append(r + len(program))
        return registers

    def getProgramLimitRegisters(self):
        registers = []
        rcl = self.getCodeLimitRegisters()
        for r, id_ in zip(rcl, self.mem.getDeclarationHistory()):
            registers.append(r + len(self.mem.getDeclarationHistory()[id_].getAllNames()))
        return registers
    
    def saveFilename(self, filename):
        self.filenames.append(filename)

    def saveFilePath(self, filepath):
        self.filepaths.append(filepath)

    def clear(self):
        self.filenames = []
        self.filepaths = []
        self.mem.declarationHistory.setDeclarationHistory({})