import traceback
from .dispatcher import Dispatcher
from .algorithms import *
class Scheduler:
    def __init__(self):
        self.algorithm  = None           
        self.dispatcher = Dispatcher()

    def setSlice(self, slice_): #!finish
        self.algorithm.setSlice(slice_)

    def getSchedulerReport(self):
        print("\n")
        print("Algoritmo: ", type(self.getAlgorithm()).__name__)
        print("Order: ", self.getAlgorithmOrder(),"\n")
        print(self.getAlgorithm().getTable() ,"\n")

    def setAlgorithmType(self, name): #change
        if name == 'FIFO' or name == 'fifo':
            self.setAlgorithm(FIFO(self.dispatcher.getPendingRunInstances()))
        if name == 'Priority' or name == 'priority':
            self.setAlgorithm(Priority(self.dispatcher.getPendingRunInstances()))
        if name == 'SJF' or name == 'sjf':
            self.setAlgorithm(SJF(self.dispatcher.getPendingRunInstances()))
        if name == 'SJFEX' or name == 'sjfEx' or name == 'sjfex':
            self.setAlgorithm(SJFEx(self.dispatcher.getPendingRunInstances()))
        if name == 'PriorityEx' or name == 'priorityex':
            self.setAlgorithm(PriorityEx(self.dispatcher.getPendingRunInstances()))
        if name == 'roundrobin' or name == 'RoundRobin' or name == 'RR' or name == 'rr':
            self.setAlgorithm(RoundRobin(self.dispatcher.getPendingRunInstances()))

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm
        self.algorithm.setup()

    def getAlgorithm(self):
        return self.algorithm

    def getAlgorithmOrder(self):
        return self.algorithm.getOrder()
    
    def compileFile(self, path):
        self.dispatcher.compileFile(path)

    def compileLines(self, lines):
        self.dispatcher.compileLines(lines)

    def run_line(self):
        self.dispatcher.run_line()

    def run_all(self):
        if self.getAlgorithm() == None:
            self.setAlgorithm(FIFO(self.dispatcher.getPendingRunInstances()))
        self.run()
    
    def run(self):
        try:
            self.algorithm.run()
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

    def setKernel(self, value):
        self.dispatcher.setKernel(value)

    def clean(self, memory, kernel, acu):
        self.dispatcher.clean(value)

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