from random import randint
class Time:
    # def __init__(self, quantum=5):
    def __init__(self, quantum=5):
        self.quantum                = quantum
        self.IOfunctionExceptions = {'lea', 'imprima', 'muestre'} 
        self.arrive_times_history = {}
        self.cpu_burst_history    = {}
        self.arrive_times         = {}
        self.cpu_burst            = {}

    def getArrivalTimesHistory(self):
        instances = self.arrive_times_history.keys()
        times     = self.arrive_times_history.items()
        formated  = []
        for instance, time in zip(instances, times):
            name = instance.getFilename()
            formated.append((name,time[1]))
        return formated

    def getArrivalTimes(self):
        return self.arrive_times 

    def getCpuBurstsHistory(self):
        instances = self.cpu_burst_history.keys()
        times     = self.cpu_burst_history.items()
        formated  = []
        for instance, time in zip(instances, times):
            name = instance.getFilename()
            formated.append((name,time[1]))
        return formated

    def getCpuBursts(self):
        return self.cpu_burst 

    def getTimeToFinish(self):
        return self.time_to_finish

    def calculate_program_time(self, run_instance):
        program = self.getProgramFromInstance(run_instance)
        instructions_with_times = []
        timeOnly                = []
        time = None
        total = 0
        for line in program:
            if line[0] in self.IOfunctionExceptions:
                time = randint(1,9)
            else:
                time = 1
            total += time
        return total

    def getProgramFromInstance(self, instance):
        declaration = instance.progDefs.getDeclaration()
        mem         = instance.getMemory()
        return mem.getInstructionFromDeclaration(declaration)

    def setSlice(self, quantum):
        self.quantum = quantum
    
    def getQuantum(self):
        return self.quantum

    def checkIfTheresTime(self, instance):
        program_time = self.cpu_burst_history[instance]
        if program_time <=self.quantum:
            self.quantum -= program_time
            return True
        return False

    def checkIfTheresTimeExpro(self, instance):
        program_time = self.cpu_burst[instance]
        if program_time <=self.quantum:
            self.quantum -= program_time
            print(f"program_time: {program_time}")
            print(f"current quantum: {self.quantum}")
            return True
        return False
    
    def setCpuBursts(self, run_instances):
            for instance in run_instances:
                self.cpu_burst[instance] = self.calculate_program_time(instance)
            self.cpu_burst_history = self.cpu_burst.copy()

    def setArriveTime(self, run_instance, prev_time):
        program = self.getProgramFromInstance(run_instance)
        num_instructions = 0
        for line in program:
            num_instructions += 1
        return round((prev_time + num_instructions) / 4)

    def setArrivalTimes(self, run_instances):
        time = 0
        first = True
        for instance in run_instances:
            if first:
                self.arrive_times[instance] = time
                first = False
                continue
            time = self.setArriveTime(instance, time)
            self.arrive_times[instance] = time
        self.arrive_times_history = self.arrive_times.copy()
    
    def getArrivalTime(self, instance):
        return self.arrive_times_history[instance]

    def getCpuBurst(self, instance):
        return self.cpu_burst_history[instance]

    def getCurrentCpuBurst(self, instance):
        return self.cpu_burst[instance]
    
    def substractFromCPU(self, instance, quantity):
        if quantity >= 0:
            self.cpu_burst[instance] -= quantity
        else:
            self.cpu_burst[instance] = 0

    def getSortedArrivalTimes(self):
        arrive_times = self.getArrivalTimes()
        possible = []
        arrive_times = list(arrive_times.items())
        arrive_times.sort(key= lambda tuple_: tuple_[1])
        return arrive_times

    def getTimeToRunAllInstances(self):
        sum_ = 0
        for instance, cpu in self.cpu_burst_history.items():
            sum_ += cpu
        return sum_