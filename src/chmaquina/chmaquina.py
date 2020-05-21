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
        self.fileInfo.saveDeclaration(self.declaration)
    
    def getVariables(self):
        return self.fileInfo.getVariables()

    def getTags(self):
        return self.fileInfo.getTags()

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
        self.fileInfo.saveDeclaration(self.declaration, True)

    def getPrograms(self): # create new class to encapsulate program related procedures
        return self.mem.programs_saved()

    def getRegisters(self):
        return self.fileInfo.getRegisters()
    
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