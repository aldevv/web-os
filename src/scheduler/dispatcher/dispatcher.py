from .factory import Factory
import copy

class Dispatcher:
    def __init__(self, memory_available=80,kernel=10):
        self.mem                = Factory.createMemory(memory_available,kernel)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
        self.original           = [copy.deepcopy(self.mem), None, None, None]

    def resetMaquina(self):
        self.mem, self.declaration, self.compiler, self.instructionRunner = self.original
        self.original = [copy.deepcopy(self.mem), None, None, None]

    def appendRunInstance(self, runner_instance):
        queue = self.mem.getQueues()
        queue.appendRunInstance(runner_instance)
    
    def getPendingRunInstances(self):
        queues = self.mem.getQueues()
        return queues.getPendingRunInstances()

    def getMemory(self):
        return self.mem

    def getStdout(self):
        stdout = []
        dataStream = self.mem.getDataStream()
        stdout_all_instances = dataStream.stdout
        queues = self.mem.getQueues()
        run_instances = queues.getRunInstances()
        for run_instance in run_instances:
            declaration = run_instance.progDefs.getDeclaration()
            if declaration in stdout_all_instances:
                stdout.extend(dataStream.getStdout(declaration))
        return stdout

    def getPrinter(self):
        printer = []
        dataStream = self.mem.getDataStream()
        printer_all_instances = dataStream.printer
        queues = self.mem.getQueues()
        run_instances = queues.getRunInstances()
        for run_instance in run_instances:
            declaration = run_instance.progDefs.getDeclaration()
            if declaration in printer_all_instances:
                printer.extend(dataStream.getPrinter(declaration))
        return printer

    def getRunInstances(self):
        queues = self.mem.getQueues()
        return queues.getRunInstances()

    def appendCompileInstance(self, compile_instance):
        queue = self.mem.getQueues()
        queue.appendCompileInstance(compile_instance)

    def getCompileInstances(self):
        queue = self.mem.getQueues()
        return queue.getCompileInstances()

    def compileFile(self, path):
        self.declaration       = Factory.createDeclaration(self.mem)
        self.compiler          = Factory.createCompiler(self.mem, self.declaration)
        self.appendCompileInstance(self.compiler)
        self.compiler.compileFile(path)
        # the variables and tags for the program compiled
        self.mem.saveDeclaration(self.declaration)
        self.mem.addDeclarationToPending(self.declaration)
        self.createRunners()
    
    def compileLines(self, lines):
        self.declaration = Factory.createDeclaration(self.mem)
        self.createCompilerIfNone()
        self.compiler.compileLines(lines)
        self.mem.saveDeclaration(self.declaration)
        self.mem.addDeclarationToPending(self.declaration)
        self.createRunners()

    def createDeclarationIfNone(self):
        if(self.declaration == None):
            self.declaration = Factory.createDeclaration(self.mem)

    def createCompilerIfNone(self):
        if(self.compiler == None):
            self.compiler    = Factory.createCompiler(self.mem, self.declaration)

    def createRunnerIfNone(self):
        if(self.instructionRunner == None):
            pendingDeclarations = self.mem.getPendingDeclarations()
            print("this declaration's variables: ", pendingDeclarations[0].getVariables())
            self.instructionRunner    = Factory.createInstructionRunner(self.mem, pendingDeclarations.pop(0))

            #!save declaration?

    def createRunners(self):
        all_declarations = self.mem.declarationHistory
        num_declaration_pending = len(all_declarations.getPending())
        pending = all_declarations.getPending()
        # print("num declarations pending: ", num_declaration_pending)
        for i in range(num_declaration_pending):
            # print("the pending variables: before ", pending[0].getVariables())
            self.instructionRunner = Factory.createInstructionRunner(self.mem, pending.pop(0))
            self.appendRunInstance(self.instructionRunner)

        # return self.mem.getVariablesNoPos()

        # return self.mem.getTagsNoPos()

    def getSteps(self): #!
        #TODO make the steps for each compiler and instructionRunner made
        pass
        # steps = []
        # instructions_compiled = []
        # instructions_ran      =  []
        # num_progs = len(self.getCompileInstances())
        # compilers = self.getCompileInstances()
        # runners = self.getRunInstances()
        # for i in range(num_progs):
        #     declaration = runners[i].progDefs.getDeclaration()
        #     if self.mem.getSteps(declaration) == []:
        #         continue
        #     steps += self.mem.getSteps(declaration)
        #     instructions_compiled += compilers[i].get_declarations_executed_history()
        #     instructions_ran      += runners[i].get_operators_executed_history()
        # all_ = instructions_compiled + instructions_ran
        # print(f"all_: {all_}, steps: {steps}")
        # return "\n".join(["line: " + str(a[0]) + " " + str(a[1][0]) + " " + str(a[1][1]) + " | " + str(b) for a, b in zip(all_, steps)])
    
    def getFileLengthNoComments(self):
        return self.compiler.getProgramLengthNoComments()

    def setMemory(self, value):
        self.mem                = Factory.createMemory(value, self.mem.getKernel())
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None

    def setKernel(self, value):
        self.mem                = Factory.createMemory(self.mem.initial_memory, value)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
    
    def clean(self, memory, kernel, acu):
        self.mem                = Factory.createMemory(memory, kernel)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None