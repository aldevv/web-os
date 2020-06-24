from .algorithm import Algorithm
from tabulate   import tabulate
import traceback

class SJF(Algorithm):
    #Shortest job first
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances     = run_instances
        self.ordered_instances = None

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

    def orderRunInstancesByTimeLeft(self):
        self.orderRunInstancesByArrival()
        num_instances = len(self.run_instances)
        new_order_run_instances = []
        current_time = 0
        for i in range(num_instances):
            possible = self.runnableInstances(current_time)
            instance = self.findShortestJob(possible)
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

    def findShortestJob(self, instances_possible):
        shortest = 99999999
        answer  = None
        for instance in instances_possible:
            if self.time.getCpuBurst(instance) < shortest:
                answer = instance
                shortest = self.time.getCpuBurst(instance)
        return answer

    def extractFromTimeAndCpu(self, instance): #TODO make it work without time object, but a queue object wrapper that uses cpu, time, and runners
        times    = self.time.getArrivalTimes()
        cpu      = self.time.getCpuBursts()
        times    = times.pop(instance, None)
        cpu      = cpu.pop(instance, None)
        return times, cpu

    def setup(self):
        self.orderRunInstancesByTimeLeft()
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