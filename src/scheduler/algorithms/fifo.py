from .algorithm import Algorithm
from tabulate   import tabulate
import traceback

class FIFO(Algorithm):
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances     = run_instances
        self.ordered_instances = None
        self.currentLineRunInstance   = None

    def getRunInstances(self):
        return self.run_instances

    def getOrder(self):
        instances = self.ordered_instances
        names    = []
        for item in instances:
            names.append(item.getFilename())

        concat = []
        id_ = 1
        for name in names:
            concat.append((id_, name))
            id_ += 1
        return concat

    def orderRunInstances(self):
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)
        arrive_times = list(self.time.arrive_times.items())
        arrive_times.sort(key= lambda tuple: tuple[1])
        
        self.run_instances.clear()
        for elem in arrive_times:
            self.run_instances.append(elem[0])
        self.ordered_instances = self.run_instances.copy()

    def setup(self):
        self.orderRunInstances()
        self.orderPendingInstructions(self.run_instances)
        

    def run(self):
        num_instances = len(self.run_instances)
        instance = None
        for i in range(num_instances):
            instance = self.run_instances.pop(0)
            instance.run_all()
    
    def runLine(self):
        if self.currentLineRunInstance == None and len(self.run_instances) == 0:
            print("nothing more to run")
            return 
        else:
            if self.currentLineRunInstance == None:
                self.currentLineRunInstance = self.run_instances.pop(0)

        itRan = self.currentLineRunInstance.run_line()
        declaration = self.currentLineRunInstance.progDefs.getDeclaration() 
        dataStream = self.memory.getDataStream()
        dataStream.clearSteps() 
        if itRan:
            stepsInRunner = self.currentLineRunInstance.get_operators_executed_history() 
            step = stepsInRunner.pop(0)
            line = step[0]
            instructionName = step[1]
            instructionName = " ".join(step[1])
            message = "line: " + str(line) + " " + str(instructionName) + " | " + self.memory.getSteps(declaration).pop() #!
            print(f"entered here, where it ran, the message is: {message}")
            dataStream.appendStep(declaration, message)
        else:
            queues = self.memory.getQueues()
            compiler = queues.getCompilerFromDeclaration(declaration)
            stepsInCompiler = compiler.get_declarations_executed_history()
            if len(stepsInCompiler) > 0:
                step = stepsInCompiler.pop(0)
                line = step[0]
                instructionName = step[1]
                instructionName = " ".join(step[1])
                message = "line: " + str(line) + " " + str(instructionName) + " | " + self.memory.getSteps(declaration).pop(0) #!
                print(f"entered here, where it did not run, the message is: {message}")
                dataStream.appendStep(declaration, message)

        current_line = self.currentLineRunInstance.getCurrentLine()
        length_program = len(self.memory.getInstructionFromDeclaration(declaration))
        finished = True if  current_line == length_program else False

        if finished: 
            self.currentLineRunInstance = None


    def getTable(self):
        instances = self.ordered_instances
        arrival   = []
        for instance in instances:
            arrival.append(self.time.getArrivalTime(instance))

        cpu  = []
        for instance in instances:
            cpu.append(self.time.getCpuBurst(instance))

        table = []
        for instance,arr, cp in zip(instances,arrival,cpu):
            table.append([instance.getFilename(), arr, cp])
        return tabulate(table, headers=['Nombre', 'Tiempo de llegada', 'Rafaga de cpu'], tablefmt='orgtbl')