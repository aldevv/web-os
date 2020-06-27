from .algorithm import Algorithm
from random     import randint
from tabulate   import tabulate
import traceback

class Priority(Algorithm):
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances          = run_instances
        self.ordered_instances      = None
        self.priorities             = {}

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
            instance = self.findHighestPriority(possible)
            _,cpu    = self.extractFromTimeAndCpu(instance)
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
        arrive_times = self.time.getArrivalTimes()
        possible = []
        arrive_times = list(arrive_times.items())
        arrive_times.sort(key= lambda tuple_: tuple_[1])
        for time in arrive_times:
            if time[1] <= current_time:
                possible.append(time[0])
        return possible

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
        
        try:
            num_instances = len(self.run_instances)
            instance = None
            for i in range(num_instances):
                instance = self.run_instances.pop(0)
                if self.time.checkIfTheresTime(instance):
                    instance.run_all()
                else:
                    raise Exception()
        except Exception as err:
            print(traceback.format_exc())
            print("not enough time!, program: ",instance.getFilename(), ", cpu burst: ", self.time.cpu_burst[instance], " vs slice: ", self.time.getSlice())






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