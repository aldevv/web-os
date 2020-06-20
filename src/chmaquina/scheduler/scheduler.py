import traceback
class Scheduler:
    def __init__(self):
        self.run_instances         = []
        self.compile_instances     = []
        self.pending_run_instances = []
        self.algorithm             = None

    def setSlice(self, slice_):
        self.algorithm.setSlice(slice_)

    def getSchedulerReport(self):
        print("Algoritmo: ", type(self.getAlgorithm()).__name__)
        print("Order: ", self.getAlgorithmOrder(),"\n")
        print(self.getAlgorithm().getTable() ,"\n")

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
        self.algorithm.setup()

    def getAlgorithm(self):
        return self.algorithm

    def getAlgorithmOrder(self):
        return self.algorithm.getOrder()
    
    def getCompilerFromDeclaration(self, declaration):
        for compiler in self.compile_instances:
            if compiler.progDefs.getDeclaration() == declaration:
                return compiler

    def run(self):

        try:
            self.algorithm.run()
        except Exception as err:
            print(traceback.format_exc())
            print("Hubo un error en runtime ", err.args, err)