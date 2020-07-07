class Queue:
    def __init__(self):
        self.compile_instances  = []
        self.run_instances      = []
        self.pending_run_instances = []
        self.pending_programs   = []

    def setPendingPrograms(self, instructions):
        self.pending_programs = instructions
    
    def addToPending(self, program):
        self.pending_programs.append(program)

    def getPendingPrograms(self):
        return self.pending_programs

    def appendCompileInstance(self, compile_instance):
        self.compile_instances.append(compile_instance)

    def getCompileInstances(self):
        return self.compile_instances

    def getCompilerFromDeclaration(self, declaration):
        for compiler in self.compile_instances:
            if compiler.progDefs.getDeclaration() == declaration:
                return compiler

    def getRunnerFromDeclaration(self, declaration):
        for runner in self.run_instances:
            if runner.progDefs.getDeclaration() == declaration:
                return runner

    def appendRunInstance(self, runner_instance):
        self.run_instances.append(runner_instance)
        self.pending_run_instances.append(runner_instance)

    def getRunInstances(self):
        return self.run_instances

    def getPendingRunInstances(self):
        return self.pending_run_instances

    def clearPendingRunInstances(self):
        self.pending_run_instances = []