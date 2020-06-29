from .factory import Factory
import copy

class Dispatcher:
    def __init__(self, memory_available=80,kernel=10):
        self.mem                = Factory.createMemory(memory_available,kernel)
        self.declaration        = None
        self.compiler           = None
        self.instructionRunner  = None
        self.original           = [copy.deepcopy(self.mem), None, None, None]
        self.compile_instances  = []
        self.run_instances      = []
        self.pending_run_instances = []

    def resetMaquina(self):
        self.mem, self.declaration, self.compiler, self.instructionRunner = self.original
        self.original = [copy.deepcopy(self.mem), None, None, None]

    def appendRunInstance(self, runner_instance):
        self.run_instances.append(runner_instance)
        self.pending_run_instances.append(runner_instance)
    
    def getPendingRunInstances(self):
        return self.pending_run_instances

    def getMemory(self):
        return self.mem

    def getStdout(self):
        stdout = []
        for runner_instance in self.run_instances:
            if len(runner_instance.getStdout()) > 0:
                stdout.extend(runner_instance.getStdout())
        return stdout

    def getPrinter(self):
        printer = []
        for runner_instance in self.run_instances:
            if len(runner_instance.getPrinter()) > 0:
                printer.extend(runner_instance.getPrinter())
        return printer

    def getRunInstances(self):
        return self.run_instances

    def appendCompileInstance(self, compile_instance):
        self.compile_instances.append(compile_instance)

    def getCompileInstances(self):
        return self.compile_instances

    def getCompilerFromDeclaration(self, declaration):
        for compiler in self.compile_instances:
            if compiler.progDefs.getDeclaration() == declaration:
                return compiler

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

    def run_line(self):
        self.createRunnerIfNone() ## need to create it according to the first declaration in the first file sent
        declaration = self.instructionRunner.progDefs.getDeclaration()
        compiler = self.getCompilerFromDeclaration(declaration)
        stepsInCompiler = compiler.get_declarations_executed_history()

        if(self.instructionRunner.getCurrentLine() == None):
            self.instructionRunner.current_line = 0
        step = None
        programs_to_run = self.mem.pending_programs.copy()
        didItRun = self.instructionRunner.run_line()
        # print("did it run ", didItRun, "\n")
        if  didItRun == True: #true si era un operador, false si era declaracion
            stepsInRunner = self.instructionRunner.get_operators_executed_history()
            step = stepsInRunner.pop(0)
            line = step[0]
            instructionName = step[1]
            instructionName = " ".join(step[1])
            message = "line: " + str(line) + " " + str(instructionName) + " | " + self.mem.getSteps().pop()
            # print("message: ", message)
            self.instructionRunner.appendStdout(message)
            print("stdout:", self.getStdout(), "\n")
            if self.instructionRunner not in self.getRunInstances():
                self.appendRunInstance(self.instructionRunner)
        else:
            if len(stepsInCompiler) > 0:
                step = stepsInCompiler.pop(0)
                line = step[0]
                instructionName = step[1]
                instructionName = " ".join(step[1])
                message = "line: " + str(line) + " " + str(instructionName) + " | " + self.mem.getSteps().pop(0)
                self.instructionRunner.appendStdout(message)

                if self.instructionRunner not in self.getRunInstances():
                    self.appendRunInstance(self.instructionRunner)

        if len(self.mem.pending_programs) != len(programs_to_run):
            pendingDeclarations = self.mem.getPendingDeclarations()
            if pendingDeclarations != []:
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

    def getSteps(self): #! only shows the last program steps, but all the steps are saved in mem
        #TODO make the steps for each compiler and instructionRunner made
        steps = self.mem.getSteps()
        # print(self.mem.getSteps())
        if steps == []:
            return None
        instructions_compiled = []
        instructions_ran      =  []
        num_progs = len(self.getCompileInstances())
        compilers = self.getCompileInstances()
        runners = self.getRunInstances()
        for i in range(num_progs):
            instructions_compiled += compilers[i].get_declarations_executed_history()
            instructions_ran      += runners[i].get_operators_executed_history()
        all_ = instructions_compiled + instructions_ran
        return "\n".join(["line: " + str(a[0]) + " " + str(a[1][0]) + " " + str(a[1][1]) + " | " + str(b) for a, b in zip(all_, steps)])
    
    def getFileLengthNoComments(self):
        return self.compiler.getProgramLengthNoComments()

    def setMemory(self, value):
        self.mem                = Factory.createMemory(value, self.mem.getKernel(), 0)
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