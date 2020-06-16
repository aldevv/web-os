from .factory import Factory
from .scheduler.algorithms import FIFO
import copy

class Chmaquina:
    def __init__(self, memory_available=80,kernel=10, acumulador=0):
        self.mem                = Factory.createMemory(memory_available,kernel, acumulador)
        self.fileInfo           = Factory.createFileInfo(self.mem)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
        self.scheduler          = Factory.createScheduler()
        self.original           = [copy.deepcopy(self.mem), copy.deepcopy(self.fileInfo), None, None, None, copy.deepcopy(self.scheduler)]

    def resetMaquina(self):
        self.mem, self.fileInfo, self.declaration, self.compiler, self.instructionRunner, self.scheduler = self.original
        self.original           = [copy.deepcopy(self.mem), copy.deepcopy(self.fileInfo), None, None, None, copy.deepcopy(self.scheduler)]

    def compileFile(self, path):
        self.declaration       = Factory.createDeclaration(self.mem)
        self.compiler          = Factory.createCompiler(self.mem, self.declaration)
        self.compiler.compileFile(path)
        # the variables and tags for the program compiled
        self.mem.saveDeclaration(self.declaration)
        self.mem.addDeclarationToPending(self.declaration)
    
    def compileLines(self, lines):
        self.declaration       = Factory.createDeclaration(self.mem)
        self.createCompilerIfNone()
        self.compiler.compileLines(lines)
        self.mem.saveDeclaration(self.declaration)
        self.mem.addDeclarationToPending(self.declaration)

    def createDeclarationIfNone(self):
        if(self.declaration == None):
            self.declaration = Factory.createDeclaration(self.mem)

    def createCompilerIfNone(self):
        if(self.compiler == None):
            self.compiler    = Factory.createCompiler(self.mem, self.declaration)

    def createRunnerIfNone(self):
        if(self.instructionRunner == None):
            self.instructionRunner    = Factory.createInstructionRunner(self.mem, self.declaration)

    def run_line(self):
        self.createRunnerIfNone()
        if(self.instructionRunner.getCurrentLine() == None):
            self.instructionRunner.current_line = 0
        didItRun = self.instructionRunner.run_line()
        if  didItRun == True: #true si era un operador, false si era declaracion
            stepsInRunner = self.instructionRunner.get_operators_executed_history()
            step = stepsInRunner.pop(0)
            line = step[0]
            instructionName = step[1]
            instructionName = " ".join(step[1])
            self.instructionRunner.appendStdout( "line: " + str(line) + " " + str(instructionName) + " | " + self.mem.getSteps().pop())
        else:
            stepsInCompiler = self.compiler.get_declarations_executed_history()
            if len(stepsInCompiler) > 0:
                step = stepsInCompiler.pop(0)
                line = step[0]
                instructionName = " ".join(step[1])
                self.instructionRunner.appendStdout( "line: " + str(line) + " " + str(instructionName) + " | " + self.mem.getSteps().pop(0))

        #!save declaration?

    def run_all(self):
        self.createRunners()
        self.scheduler.setAlgorithm(FIFO(self.scheduler.pending_run_instances))
        self.scheduler.run()

    def createRunners(self):
        all_declarations = self.mem.declarationHistory
        num_declaration_pending = len(all_declarations.getPending())
        pending = all_declarations.getPending()
        # print("num declarations pending: ", num_declaration_pending)
        for i in range(num_declaration_pending):
            # print("the pending variables: before ", pending[0].getVariables())
            self.instructionRunner = Factory.createInstructionRunner(self.mem, pending.pop(0))
            self.scheduler.appendRunInstance(self.instructionRunner)

    def getVariables(self): #!change in front!
        return self.mem.getVariables()
        # return self.mem.getVariablesNoPos()

    def getTags(self):
        return self.mem.getTags()
        # return self.mem.getTagsNoPos()

    def getMemory(self): 
        return self.mem.getMemory()

    def getPrograms(self): # create new class to encapsulate program related procedures
        return self.mem.get_programs()

    def getRegisters(self):
        return self.fileInfo.getRegisters()

    def getAcumulador(self):
        return self.mem.getAcumulador()
    
    def getStdout(self):
        # return self.instructionRunner.getStdout()  # get it from the scheduler!
        return self.scheduler.getStdout()  # get it from the scheduler!

    def getPrinter(self):
        # return self.instructionRunner.getPrinter()
        return self.scheduler.getPrinter()  
    
    def getSteps(self): #! only shows the last program steps, but all the steps are saved in mem
        #TODO make the steps for each compiler and instructionRunner made
        steps = self.mem.getSteps()
        # print(self.mem.getSteps())
        if steps == []:
            return None
        instructions_compiled = self.compiler.get_declarations_executed_history()
        instructions_ran = self.instructionRunner.get_operators_executed_history()
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