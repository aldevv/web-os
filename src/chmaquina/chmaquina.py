from .factory import Factory

class Chmaquina:
    def __init__(self, memory_available=80,kernel=10, acumulador=0):
        self.mem                = Factory.createMemory(memory_available,kernel, acumulador)
        self.fileInfo           = Factory.createFileInfo(self.mem)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None

    def compileFile(self, path):
        self.declaration       = Factory.createDeclaration(self.mem)
        self.compiler          = Factory.createCompiler(self.mem, self.declaration)
        self.compiler.compileFile(path)
        # the variables and tags for the program compiled
        self.mem.saveDeclaration(self.declaration)
    
    def compileLines(self, lines):
        self.createDeclarationIfNone()
        self.createCompilerIfNone()
        self.compiler.compileLines(lines)

    def createDeclarationIfNone(self):
        if(self.declaration == None):
            self.declaration = Factory.createDeclaration(self.mem)

    def createCompilerIfNone(self):
        if(self.compiler == None):
            self.compiler    = Factory.createCompiler(self.mem, self.declaration)

    def createRunnerIfNone(self):
        if(self.instructionRunner == None):
            self.instructionRunner    = Factory.createInstructionRunner(self.mem, self.declaration)

    def run_line(self, atStart=False):
        self.createRunnerIfNone()
        ranOperator = self.instructionRunner.run_line(atStart)
        return True if ranOperator == True else False
        #!save declaration?

    def run_all(self):
        self.instructionRunner = Factory.createInstructionRunner(self.mem, self.declaration)
        self.instructionRunner.run_all()
        self.mem.saveDeclaration(self.declaration, True)

    def getVariables(self): #!change in front!
        # return self.mem.getVariables()
        return self.mem.getVariablesNoPos()

    def getTags(self):
        # return self.mem.getTags()
        return self.mem.getTagsNoPos()

    def getMemory(self): 
        return self.mem.getMemory()

    def getPrograms(self): # create new class to encapsulate program related procedures
        return self.mem.get_programs()

    def getRegisters(self):
        return self.fileInfo.getRegisters()

    def getAcumulador(self):
        return self.mem.getAcumulador()
    
    def getStdout(self):
        return self.instructionRunner.getStdout()
    
    def getSteps(self):
        steps = self.mem.getSteps()
        if steps == []:
            return None
        instructions_compiled = self.compiler.get_program_history()
        instructions_ran = self.instructionRunner.get_program_history()
        all_ = instructions_compiled +instructions_ran
        return "\n".join(["line: " + str(a[0]) + " " + str(a[1][0]) + " " + str(a[1][1]) + " | " + str(b) for a, b in zip(all_, steps)])
    
    def getFileLengthNoComments(self):
        return self.compiler.getProgramLengthNoComments()

    def setMemory(self, value):
        self.mem                = Factory.createMemory(value, self.mem.getKernel(), 0)
        self.fileInfo           = Factory.createFileInfo(self.mem)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None

    def setKernel(self, value):
        self.mem                = Factory.createMemory(self.mem.initial_memory, value,0)
        self.fileInfo           = Factory.createFileInfo(self.mem)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None

    def setAcumulador(self, value):
        self.mem                = Factory.createMemory(self.mem.initial_memory, self.mem.getKernel(), value)
        self.fileInfo           = Factory.createFileInfo(self.mem)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
    
    def clean(self, memory, kernel, acu):
        self.mem                = Factory.createMemory(memory, kernel, acu)
        self.fileInfo           = Factory.createFileInfo(self.mem)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None


    def getMemoryAvailable(self):
        return self.mem.get_available_memory()

    def getMemoryUsed(self):
        return self.mem.get_used_memory()