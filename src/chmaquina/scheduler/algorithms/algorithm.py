from ..time import Time

class Algorithm:
    def __init__(self):
        self.time           = Time()
        self.memory         = None

    def getTime(self):
        return self.time

    def setup(self):
        # setup before run
        pass

    def run(self):
        # how it runs
        pass


    def getMemory(self, run_instances):
        return run_instances[0].getMemory()

    def orderPendingInstructions(self, run_instances):
        self.memory = self.getMemory(run_instances)
        self.memory.orderPendingInstructions(run_instances)