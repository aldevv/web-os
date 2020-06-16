
class Scheduler:
    def __init__(self):
        self.run_instances                = []
        self.compile_instances            = []
        self.pending_run_instances        = []
        self.programs_to_run = None
        self.algorithm       = None

    def appendRunInstance(self, runner_instance):
        self.run_instances.append(runner_instance)
        self.pending_run_instances.append(runner_instance)

    def appendCompileInstance(self, compile_instance):
        self.compile_instances.append(compile_instance)

    def getRunInstances(self):
        return self.run_instances

    def getCompileInstances(self):
        return self.compile_instances

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

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm
    
    def run(self):
        self.algorithm.run()
    
    def getCompilerFromDeclaration(self, declaration):
        for compiler in self.compile_instances:
            if compiler.progDefs.getDeclaration() == declaration:
                return compiler