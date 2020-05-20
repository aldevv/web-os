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
    
    def getInstructions(self): #sin comments
        return len(self.mem.memory_slots)
    
    def getBaseRegister(self):
        return self.mem.getKernel() + 1 # del acumulador

    def getCodeLimitRegister(self):
        return self.mem.getKernel() + self.getInstructions()

    def getProgramLimitRegister(self):
        return self.mem.getKernel() + self.getInstructions() + len(self.variables.all_data_names)