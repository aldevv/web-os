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
    
    def compileFile(self, path):
        self.dispatcher.compileFile(path)

    def compileLines(self, lines):
        self.dispatcher.compileLines(lines)

    def run_line(self, algorithm="roundrobin"):
    # def run_line(self, algorithm="RoundRobin"):
        if algorithm.lower() in self.ex_algorithms:
            print("entered ex")
            self.run_line_ex(algorithm)
        else:
            print("entered normal")
            self.run_line_normal(algorithm)



    def run_line_ex(self, algorithm):
        if len(self.dispatcher.getPendingRunInstances()) == 0:
            print("no programs pending")
            return
        print(f"pending programs before run line: {len(self.dispatcher.getPendingRunInstances())}")
        self.setAlgorithmType(algorithm) #should become none after done running all instructions
        self.run("line")

    def run_line_normal(self, algorithm):
        if self.algorithm == None:
            self.setAlgorithmType(algorithm) #should become none after done running all instructions
        self.run("line")

    def setAlgorithmType(self, name): #change
        print("self.algorithm: ", self.algorithm)
        print("pendinglefttorun left to run: ", self.dispatcher.getPendingRunInstances())
        if self.algorithm != None:
            print("instances left to run: ", self.instancesLeftToRun())
            if self.instancesLeftToRun():
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
