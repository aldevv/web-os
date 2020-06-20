from .algorithm import Algorithm
from random import randint

class Priority(Algorithm):
    def __init__(self, run_instances, expropiativo=False):
        self.run_instances          = run_instances
        self.priotity_and_instances = None
        self.expropiativo           = expropiativo

    def setPriorities(self):
        priority_queue = self.genPriorities() # [(priority_num, run_instance), ...]
        if not self.expropiativo:
            # sort according to priority
            priority_queue.sort(key= lambda tuple: tuple[0], reverse=True)
            self.priotity_and_instances = priority_queue
            #put the runner instance in the correct order
        # else:

    def genPriorities(self):
        priority_queue = []
        for instance in self.run_instances:
            priority_queue.append((randint(0,100), instance)) # (priority, run_instance), example: (8, run_instance of factorial.ch)
        return priority_queue
        
    def orderRunInstances(self):
        self.run_instances.clear()
        for i in range(len(self.priotity_and_instances)):
            self.run_instances.append(self.priotity_and_instances[i][1])

    def getInfo(self):
        return self.priotity_and_instances

    def setup(self):
        self.setPriorities()
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)
        self.orderRunInstances()
        self.orderPendingInstructions(self.run_instances)

    def run(self):
        num_instances = len(self.run_instances)
        for i in range(num_instances):
            instance = self.run_instances.pop(0)
            instance.run_all()
    