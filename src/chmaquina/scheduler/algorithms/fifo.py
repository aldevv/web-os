from .algorithm import Algorithm
import traceback

class FIFO(Algorithm):
    def __init__(self, run_instances):
        super().__init__()
        self.run_instances = run_instances

    def getInfo(self):
        arrivals = self.time.getArrivalTimes()
        names    = []
        for item in arrivals:
            names.append(item[0])

        concat = []
        id_ = 1
        for name in names:
            concat.append((id_, name))
            id_ += 1
        return concat

    def printOrder(self):
        print("order run")
        for instance in self.run_instances:
            file = instance.getFilename()
            print(file)

    def setup(self):
        self.orderPendingInstructions(self.run_instances)
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)

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


