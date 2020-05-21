from .factory import Factory

class Chmaquina:
    def __init__(self, memory_available=80,kernel=10, acumulador=0):
        self.mem                = Factory.createMemory(memory_available,kernel, acumulador)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
        self.declarationHistory = {}
        self.filenames          = []

    def compileFile(self, path):
        self.declaration       = Factory.createDeclaration(self.mem)
        self.compiler          = Factory.createCompiler(self.mem, self.declaration)
        self.compiler.compileFile(path)
        self.saveDeclaration(self.declaration)
    
    def saveDeclaration(self, declaration, update=None):
        if update == True:
            last_element = len(self.declarationHistory) - 1
            self.declarationHistory[last_element] = declaration
        else:
            self.declarationHistory[len(self.declarationHistory)] = declaration
    
    def getVariablesHistory(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getVariables())
        return all_

    def getTagsHistory(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getTags())
        return all_

    def compileLines(self, lines):
        if(self.declaration == None):
            self.declaration = Factory.createDeclaration(self.mem)
        if(self.compiler == None):
            self.compiler    = Factory.createCompiler(self.mem, self.declaration)
        self.mem.setMemoryBeforeCompile()
        for instruction in lines:
            self.compiler.parse_and_compile_line(instruction)
        self.mem.saveProgram(self.compiler.currentProgram)
        

    def run_all(self):
        self.instructionRunner = Factory.createInstructionRunner(self.mem, self.declaration)
        self.instructionRunner.run_all()
        self.saveDeclaration(self.declaration, True)

    def getVariables(self):
        return self.declaration.getVariables()

    def getTags(self):
        return self.declaration.getTags()

    def getPrograms(self): # create new class to encapsulate program related procedures
        return self.mem.programs_saved()
    
    # def getInstructionsReadable(self):
    #     return "\n".join([ str(i)+ " " + " ".join(instruction) for i, instruction in enumerate(self.mem.instructions_saved())])

    def getAcumulador(self):
        return self.mem.getAcumulador()
    
    def getStdout(self):
        return self.instructionRunner.getStdout()
    
    def getSteps(self):
        steps = self.mem.getSteps()
        instructions_compiled = self.compiler.get_program_history()
        instructions_ran = self.instructionRunner.get_program_history()
        all_ = instructions_compiled +instructions_ran
        """
        all_ = [(1, ['nueva', 'unidad', 'I', '1']), ...]
        steps = [unidad: 1, ...]
        """
        return "\n".join([str(a[0]) + " " + str(a[1][0]) + " " + str(a[1][1]) + " | " + str(b) for a, b in zip(all_, steps)])
    
    def getFileLengthNoComments(self):
        return self.compiler.getProgramLengthNoComments()

    def getMemoryAvailable(self):
        return self.mem.get_available_memory()

    def getMemoryUsed(self):
        return self.mem.get_used_memory()
    
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
    
        