from .factory import Factory
import copy

class Dispatcher:
    def __init__(self, memory_available=80,kernel=10):
        self.mem                = Factory.createMemory(memory_available,kernel)
        self.declaration        = None # for unit testing
        self.compiler           = None
        self.original           = [copy.deepcopy(self.mem), None, None]

    def resetMaquina(self):
        self.mem, self.declaration, self.compiler = self.original
        self.original = [copy.deepcopy(self.mem), None, None]

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

    def createCompilerIfNone(self):
        if(self.compiler == None):
            self.compiler    = Factory.createCompiler(self.mem, self.declaration)

    def createRunners(self):
        all_declarations = self.mem.declarationHistory #object
        pending = all_declarations.getPending()
        num_declaration_pending = len(pending)
        queue = self.mem.getQueues()
        dataStream = self.mem.getDataStream()
        for i in range(num_declaration_pending):
            instructionRunner = Factory.createInstructionRunner(self.mem, pending.pop(0))
            queue.appendRunInstance(instructionRunner)
            dataStream.appendStatus(instructionRunner, 1)

    def getSteps(self): #!
        steps = []
        dataStream = self.mem.getDataStream()
        steps_all_instances = dataStream.steps
        queues = self.mem.getQueues()
        run_instances = queues.getRunInstances()
        for run_instance in run_instances:
            declaration = run_instance.progDefs.getDeclaration()
            if declaration in steps_all_instances:
                steps.extend(dataStream.getSteps(declaration))
        return steps
    
    def getFileLengthNoComments(self):
        return self.compiler.getProgramLengthNoComments()

    def setMemory(self, value):
        self.mem                = Factory.createMemory(value, self.mem.getKernel())
        self.declaration        = None
        self.compiler           = None

    def setKernel(self, value):
        self.mem                = Factory.createMemory(self.mem.initial_memory, value)
        self.declaration        = None
        self.compiler           = None
    
    def clean(self, memory, kernel):
        self.mem                = Factory.createMemory(memory, kernel)
        self.declaration        = None
        self.compiler           = None