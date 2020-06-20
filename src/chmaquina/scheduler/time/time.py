from random import randint
class Time:
    # def __init__(self, slice_=5):
    def __init__(self, slice_=45):
        self.slice       = slice_
        self.IOfunctionExceptions = {'lea', 'imprima', 'muestre'} 
        self.arrive_times   = {}
        self.cpu_burst      = {}

    def getArrivalTimes(self):
        return self.arrive_times

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

    def setSlice(self, slice_):
        self.slice = slice_
    
    def getSlice(self):
        return self.slice
    
    def timeLimit(self):
        return self.slice

    def checkIfTheresTime(self, instance):
        program_time = self.calculate_program_time(instance)
        if program_time <=self.slice:
            self.slice -= program_time
            return True
        return False
    
    def setCpuBursts(self, run_instances):
            for instance in run_instances:
                self.cpu_burst[instance] = self.calculate_program_time(instance)

    def arriveTime(self, run_instance, prev_time):
        program = self.getProgramFromInstance(run_instance)
        num_instructions = 0
        for line in program:
            num_instructions += 1
        return (prev_time + num_instructions) / 4

    def setArrivalTimes(self, run_instances):
        time = 0
        for instance in run_instances:
            time = self.arriveTime(instance, time)
            self.arrive_times[instance] = time