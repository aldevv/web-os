from .algorithm import Algorithm
import traceback

class FIFO(Algorithm):
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances = run_instances
        self.memory = self.run_instances

    def getInfo(self):
        progs = self.memory.get_programs()
        concat = []
        id_ = 1
        for program in progs:
            concat.append((id_, program))
            id_ += 1
        return concat

    def setup(self):
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)
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
            print("not enough time!, program: ", self.time.calculate_program_time(instance), " vs slice: ", self.time.getSlice())


