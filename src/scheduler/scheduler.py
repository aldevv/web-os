import traceback
from .dispatcher import Dispatcher
from .algorithms import *
class Scheduler:
    def __init__(self):
        self.dispatcher = Dispatcher()
        self.default_quantum = 5
        self.algorithm  = None           
        self.ex_algorithms = {"sjfex", "priorityex", "roundrobin"}
        self.algorithms_possible = {
            "fifo": FIFO,
            "sjf": SJF,
            "priority": Priority,
            "sjfex": SJFEx,
            "priorityex": PriorityEx,
            "roundrobin": RoundRobin
        }

    def getSchedulerReport(self):
        if len(self.dispatcher.getMemory().getFileInfo().getFilenames()) == 0: #ya que no hay archivos que reportar
            return
        print("\n")
        print("Algoritmo: ", type(self.getAlgorithm()).__name__)
        print("Order: ", self.getAlgorithmOrder(),"\n")
        print(self.getAlgorithm().getTable() ,"\n")


    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm
        if self.algorithm != None:
            self.algorithm.setup()

    def getAlgorithm(self):
        return self.algorithm

    def getAlgorithmOrder(self):
        return self.algorithm.getOrder()
    
    def compileFile(self, path, algorithm=None):
        self.resetMaquinaIfAlgorithmChanged(algorithm)
        self.dispatcher.compileFile(path)

    def compileLines(self, lines):
        self.dispatcher.compileLines(lines)

    def run_line(self, algorithm="roundrobin"):
        if algorithm.lower() in self.ex_algorithms:
            print("entered ex")
            self.run_line_ex(algorithm)
        else:
            print("entered normal")
            self.run_line_normal(algorithm)

    def resetMaquinaIfAlgorithmChanged(self,algorithm):
        if self.algorithm != None and type(self.getAlgorithm()).__name__.lower() != algorithm:
            self.dispatcher.resetMaquina()

    def run_line_ex(self, algorithm):
        if len(self.dispatcher.getPendingRunInstances()) == 0:
            print("no programs pending")
            return
        print(f"pending programs before run line: {len(self.dispatcher.getPendingRunInstances())}")
        self.setAlgorithmType(algorithm, mode="line") #should become none after done running all instructions
        self.run("line")

    def run_line_normal(self, algorithm):
        if self.algorithm == None:
            self.setAlgorithmType(algorithm, mode="line") #should become none after done running all instructions
        self.run("line")

    def setAlgorithmType(self, name, mode="normal"): #change
        if self.algorithm != None:
            print("instances left to run: ", self.instancesLeftToRun()) 
            if mode == "line" and self.instancesLeftToRun():
                print("\nreturned!!!\n")
                return
        name = name.lower()
        pending_programs = self.dispatcher.getPendingRunInstances()
        if name == "roundrobin":
            self.setAlgorithm(self.algorithms_possible[name](pending_programs, self.default_quantum))
        else:
            self.setAlgorithm(self.algorithms_possible[name](pending_programs))



    def instancesLeftToRun(self):
        return len(self.algorithm.getRunInstances()) != 0

    def run_all(self, algorithm="RoundRobin"):
    # def run_all(self, algorithm="FIFO"):
        self.setAlgorithmType(algorithm)
        self.run()
    
    def run(self, type_="all"):
        try:
            if type_ == "all":
                self.algorithm.run()
                self.getSchedulerReport()
            if type_ == "line":
                self.algorithm.runLine()
        except Exception as err:
            print(traceback.format_exc())
            print("Hubo un error en runtime ", err.args, err)

    def getStdout(self):
        return self.dispatcher.getStdout()

    def getPrinter(self):
        return self.dispatcher.getPrinter()

    def getVariables(self):
        mem = self.dispatcher.getMemory()
        return mem.getVariables()

    def getTags(self):
        mem = self.dispatcher.getMemory()
        return mem.getTags()

    def getMemory(self):
        mem = self.dispatcher.getMemory()
        return mem.getMemory()

    def getPrograms(self): # create new class to encapsulate program related procedures
        mem = self.dispatcher.getMemory()
        return mem.get_programs()

    def getRegisters(self):
        mem = self.dispatcher.getMemory()
        fileInfo = mem.getFileInfo()
        return fileInfo.getRegisters()

    def getAcumulador(self):
        mem = self.dispatcher.getMemory()
        return mem.getAcumuladorLastRun()

    def getSteps(self): 
        return self.dispatcher.getSteps()

    def setMemory(self, value):
        self.dispatcher.setMemory(value)
        self.algorithm = None

    def setKernel(self, value):
        self.dispatcher.setKernel(value)
        self.algorithm = None

    def setQuantum(self, value):
        self.dispatcher.resetMaquina()
        self.default_quantum = value
        self.algorithm = None
        

    def clean(self, memory, kernel, quantum):
        self.dispatcher.clean(memory, kernel)
        self.default_quantum   = quantum
        self.algorithm = None

    def getMemoryAvailable(self):
        mem = self.dispatcher.getMemory()
        return mem.get_available_memory()

    def getMemoryUsed(self):
        mem = self.dispatcher.getMemory()
        return mem.get_used_memory()


    def getDeclaration(self):
        return self.dispatcher.declaration

    def resetMaquina(self):
        self.dispatcher.resetMaquina()
        self.algorithm = None

    def getStatus(self):
        mem = self.dispatcher.getMemory()
        dataStream = mem.getDataStream()
        array = []
        for key, value in dataStream.getStatus().items():
            array.append((key.getFilename(), value))
        return array

    def getStderr(self):
        mem = self.dispatcher.getMemory()
        dataStream = mem.getDataStream()
        array = []
        for key, value in dataStream.getStderr().items():
            array.append((key.getFilename(), value))
        return array