from .algorithm import Algorithm
from random     import randint
from tabulate   import tabulate
import traceback

class Priority(Algorithm):
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances      = run_instances
        self.ordered_instances  = None
        self.priorities         = {}
        self.aging              = {}
        self.currentLineRunInstance   = None

    def getRunInstances(self):
        return self.run_instances

    def getPriority(self, instance):
        return self.priorities[instance]

    def setPriorities(self):
        self.priorities = self.genPriorities() # [(priority_num, run_instance), ...]

    def genPriorities(self):
        priorities = {}
        for instance in self.run_instances:
            priorities[instance] = randint(0,100) # (priority, run_instance), example: (8, run_instance of factorial.ch)
        return priorities
        
    def orderRunInstancesByPriority(self):
        self.orderRunInstancesByArrival()
        # print("before") #!to see table without priority ordering
        # self.ordered_instances = self.run_instances.copy()
        # print(self.getTable())
        num_instances = len(self.run_instances)
        new_order_run_instances = []
        current_time = 0
        for i in range(num_instances):
            possible = self.runnableInstances(current_time) 
            # self.ageInstances(possible)
            print(f"possible: {self.instancesToReadable(possible)}, tiempo: {current_time}")
            instance = self.findHighestPriority(possible)
            _,cpu    = self.extractFromTimeAndCpu(instance)
            print(f"instancia mayor prioridad: {instance.getFilename()},  rafaga cpu actual: {self.time.getCpuBurst(instance)}, prioridad: {self.getPriority(instance)}\n")
            current_time += cpu
            new_order_run_instances.append(instance)
            self.run_instances.remove(instance)
        self.run_instances.clear()
        self.run_instances = new_order_run_instances
        self.ordered_instances = self.run_instances.copy()

    def orderRunInstancesByArrival(self):
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)
        arrive_times = list(self.time.arrive_times.items())
        arrive_times.sort(key= lambda tuple: tuple[1])
        
        self.run_instances.clear()
        for elem in arrive_times:
            self.run_instances.append(elem[0])
    
    def runnableInstances(self, current_time):
        possible = []
        arrive_times = self.time.getSortedArrivalTimes()
        print(f"arrive_times: {arrive_times}")
        for time in arrive_times:
            if time[1] <= current_time:
                possible.append(time[0])
        return possible


    def ageInstances(self,possible):
        for instance in possible:
            if instance not in self.aging:
                self.aging[instance] = 0
            else:
                self.aging[instance] += 1
                age_value = self.aging[instance]
                if self.age(instance, age_value):
                    self.aging[instance] = 0

    def age(self, instance, age_value):
        if age_value >= 3:
            if self.priorities[instance] + 20 <= 100:
                self.priorities[instance] += 20
            else:
                self.priorities[instance] = 100
            print(f"i did it:{instance.getFilename()}, {instance}, priority before {self.priorities[instance] -20}, priority after {self.priorities[instance]}")
            return True
        return False

    def findHighestPriority(self, instances_possible):
        highest = -1
        answer  = None
        for instance in instances_possible:
            # print(f"possible: {instance.getFilename()} priority:{self.getPriority(instance)}")
            if self.getPriority(instance) > highest:
                answer = instance
                highest = self.getPriority(instance)
        # print("\n")
        return answer

    def extractFromTimeAndCpu(self, instance): #TODO make it work without time object, but a queue object wrapper that uses cpu, time, and runners
        times    = self.time.getArrivalTimes()
        cpu      = self.time.getCpuBursts()
        times    = times.pop(instance, None)
        cpu      = cpu.pop(instance, None)
        return times, cpu

    def getOrder(self):
        return [( instance.getFilename(), self.getPriority(instance) ) for instance in self.ordered_instances]

    def setup(self):
        self.setPriorities()
        self.orderRunInstancesByPriority()
        self.orderPendingInstructions(self.run_instances)

    def run(self):
        num_instances = len(self.run_instances)
        instance = None
        for i in range(num_instances):
            instance = self.run_instances.pop(0)
            instance.run_all()

    def runLine(self):
        #this was added later
        queues = self.memory.getQueues()
        if len(queues.pending_programs) > 0:
            queues.pending_programs = []

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
        instances  = []
        arrival    = []
        cpu        = []
        priorities = []
        for instance in self.ordered_instances:
            instances.append(instance)
            arrival.append(self.time.getArrivalTime(instance))
            cpu.append(self.time.getCpuBurst(instance))
            priorities.append(self.getPriority(instance))

        table = []
        for instance,arr, cp, prio in zip(instances,arrival,cpu, priorities):
            table.append([instance.getFilename(), arr, cp, prio])
        return tabulate(table, headers=['Nombre', 'Tiempo de llegada', 'Rafaga de cpu', 'Prioridad'], tablefmt='orgtbl')