from .algorithm import Algorithm
from tabulate   import tabulate
from random     import randint
from copy       import copy
import traceback

class PriorityEx(Algorithm):
    #Shortest job first
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances     = run_instances
        self.order             = None # in order of expropiative
        self.ordered_instances = None # in arrival order
        self.num_lines_to_run_all_instances = None
        self.priorities = {}
        self.aging = {}

    def getOrder(self):
        instances = self.order
        names    = []
        for item in instances:
            names.append(item.getFilename())

        concat = []
        id_ = 1
        for name in names:
            concat.append((id_, name))
            id_ += 1
        return concat

    def orderRunInstancesByPriority(self):
        self.orderRunInstancesByArrival()
        self.ordered_instances = self.run_instances.copy()
        ######################################
        self.memory = self.getMemory(self.run_instances)
        originalInstructionDictionary = self.memory.getDeclarationInstructionDictionary()
        instructionDictionary = {}
        for key in originalInstructionDictionary:
            instructionDictionary[key] = originalInstructionDictionary[key].copy()
        timeToRunAll = self.time.getTimeToRunAllInstances()
        new_order_run_instances         = []
        num_lines_to_run_all_instances = []
        current_time     = 0
        lines_to_run = 0
        declarationHistory = self.memory.declarationHistory
        first_time = True
        prev_instance = None

        print(f"numInstructionsAllinstances: {timeToRunAll}")
        while(current_time < timeToRunAll):
            possible = self.runnableInstances(current_time) 
            self.ageInstances(possible)
            self.log(possible) 
            instance = self.findHighestPriority(possible)
            self.time.substractFromCPU(instance,  1)
            print(f"instancia mayor prioridad: {instance.getFilename()},  rafaga cpu actual: {self.time.getCurrentCpuBurst(instance)}, lineas a correr: {lines_to_run}")


            if first_time:
                prev_instance = instance 
                first_time = False

            if self.time.getCurrentCpuBurst(instance) == 0:
                # print("did it 1")
                num_lines_to_run_all_instances.append(lines_to_run)
                new_order_run_instances.append(instance)
                lines_to_run = 0
                prev_instance = instance
                current_time += 1
                print(f"checked: {self.instancesToReadable(new_order_run_instances)} ")
                continue

            if self.instanceChanged(prev_instance, instance) and self.time.getCurrentCpuBurst(prev_instance) != 0:
                # print("did it 2")
                num_lines_to_run_all_instances.append(lines_to_run)
                new_order_run_instances.append(prev_instance)
                prev_instance = instance
                lines_to_run = 0
                current_time += 1
                print(f"checked: {self.instancesToReadable(new_order_run_instances)} ")
                continue

            print(f"checked: {self.instancesToReadable(new_order_run_instances)} ")
            prev_instance = instance
            declaration = instance.progDefs.getDeclaration()
            instructions = instructionDictionary[declaration]
            print(f"instructions: {instructions}\n")
            if len(instructions) == 1:
                lines_to_run +=1
                instructionDictionary[declaration] = []
            else:
                if len(instructions) != 0:
                    instructions.pop(0)
                    instructionDictionary[declaration] = instructions
                    lines_to_run +=1
            current_time += 1
        self.run_instances = new_order_run_instances
        self.num_lines_to_run_all_instances = num_lines_to_run_all_instances

    def instanceChanged(self, prev_instance, instance):
        return prev_instance != instance


    def getNumInstructionsInAllInstances(self):
        self.memory = self.getMemory(self.run_instances)
        instructions_all_instances = self.memory.get_programs()
        totalNumInstructions = 0
        for instructions in instructions_all_instances:
            totalNumInstructions += len(instructions)
        return totalNumInstructions

    def orderRunInstancesByArrival(self):
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)
        arrive_times = list(self.time.arrive_times.items())
        arrive_times.sort(key= lambda tuple: tuple[1])
        
        self.run_instances.clear()
        for elem in arrive_times:
            self.run_instances.append(elem[0])
    
    def runnableInstances(self, current_time):
        arrive_times = self.time.getSortedArrivalTimes()
        possible = []
        for time in arrive_times:
            if time[1] <= current_time and self.time.getCurrentCpuBurst(time[0]) > 0:
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
        if age_value >= 25:
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

    def getPriority(self, instance):
        return self.priorities[instance]

    def extractFromTimeAndCpu(self, instance): #TODO make it work without time object, but a queue object wrapper that uses cpu, time, and runners
        times    = self.time.getArrivalTimes()
        cpu      = self.time.getCpuBursts()
        times    = times.pop(instance, None)
        cpu      = cpu.pop(instance, None)
        return times, cpu

    def setup(self):
        self.setPriorities()
        self.orderRunInstancesByPriority()
        
    def setPriorities(self):
        self.priorities = self.genPriorities() # [(priority_num, run_instance), ...]

    def genPriorities(self):
        priorities = {}
        for instance in self.run_instances:
            priorities[instance] = randint(0,100) # (priority, run_instance), example: (8, run_instance of factorial.ch)
        return priorities

    def run(self):
        num_instances = len(self.run_instances)
        self.order = self.run_instances.copy()
        instance = None
        for i in range(num_instances):              #! error esta aqui
            instance = self.run_instances.pop(0)
            print(f"goint to run: {instance.getFilename()}")
            instance.run_all_expro(self.num_lines_to_run_all_instances.pop(0))
        
    def log(self, possible):
        for each in possible:
            print("possible: ", each.getFilename())
        print("\n")
        for instance2,cpu in self.time.getCpuBursts().items():
            print(f"{instance2.getFilename()},  arrival: {self.time.getArrivalTime(instance2)},  cpu: {cpu}, priority: {self.getPriority(instance2)}")

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

