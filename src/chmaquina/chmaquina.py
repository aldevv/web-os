from .factory import Factory

class Chmaquina:
    def __init__(self, memory_available=80,kernel=10, acumulador=0):
        self.mem               = Factory.createMemory(memory_available,kernel, acumulador)
        self.variables         = Factory.createDeclarable(self.mem)
        self.tags              = Factory.createDeclarable(self.mem)
        self.compiler          = Factory.createCompiler(self.mem, self.variables, self.tags)
        self.instructionRunner = Factory.createInstructionRunner(self.mem, self.variables, self.tags)

    def compileFile(self, path):
        self.compiler.compileFile(path)

    def compileLine(self, line):
        self.compiler.parse_and_compile_line(line)

    def run_all(self):
        self.instructionRunner.run_all()

    def getVariables(self):
        return self.variables.getNames()

    def getTags(self):
        return self.tags.getNames()

    def getInstructions(self):
        return self.mem.instructions_saved()

    def getAcumulador(self):
        return self.mem.getAcumulador()
    
    def getStdout(self):
        return self.instructionRunner.getStdin()
    
    def getSteps(self):
        return self.mem.getSteps()