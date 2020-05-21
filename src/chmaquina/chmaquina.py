from .factory import Factory

class Chmaquina:
    def __init__(self, memory_available=80,kernel=10, acumulador=0):
        self.mem                = Factory.createMemory(memory_available,kernel, acumulador)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
        self.declarationHistory = {}

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

    def compileLines(self, lines):
        if(self.declaration == None):
            self.declaration = Factory.createDeclaration(self.mem)
        if(self.compiler == None):
            self.compiler    = Factory.createCompiler(self.mem, self.declaration)
        self.mem.setMemoryBeforeCompile()
        for instruction in lines:
            self.compiler.parse_and_compile_line(instruction)
        

    def run_all(self):
        self.instructionRunner = Factory.createInstructionRunner(self.mem, self.declaration)
        self.instructionRunner.run_all()
        self.saveDeclaration(self.declaration, True)

    def getVariables(self):
        return self.declaration.getVariables()

    def getTags(self):
        return self.declaration.getTags()

    def getInstructions(self):
        return self.mem.instructions_saved()

    def getInstructionsReadable(self):
        return "\n".join([ str(i)+ " " + " ".join(instruction) for i, instruction in enumerate(self.mem.instructions_saved())])

    def getAcumulador(self):
        return self.mem.getAcumulador()
    
    def getStdout(self):
        return self.instructionRunner.getStdout()
    
    def getSteps(self):
        steps = self.mem.getSteps()
        instructions_compiled = self.compiler.get_program_history()
        instructions_ran = self.instructionRunner.get_program_history()
        all_ = instructions_compiled +instructions_ran
        return "\n".join([str(a[0]) + " " + str(a[1][0]) + " " + str(a[1][1]) + " | " + str(b) for a, b in zip(all_, steps)])
        """
        all_ = [(1, ['nueva', 'unidad', 'I', '1']), ...]
        steps = [unidad: 1, ...]
        """
    
    def getFileLength(self):
        return self.compiler.getProgramLength()
    
    def getInstructionsLenNoComments(self): #sin comments
        return len(self.mem.memory_slots)
    
    def getBaseRegister(self):
        return self.mem.getKernel() + 1 # del acumulador

    def getCodeLimitRegister(self):
        return self.mem.getKernel() + self.getInstructionsLenNoComments()

    def getProgramLimitRegister(self):
        return self.mem.getKernel() + self.getInstructionsLenNoComments() + len(self.declaration.getAllNames())