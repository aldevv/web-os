class FIFO:
    def __init__(self, run_instances):
        self.run_instances = run_instances

    def getInfo(self):
        pass


    def orderPendingInstructions(self):
        mem = self.run_instances[0].getMemory()
        for instance in self.run_instances:
            declaration = instance.progDefs.getDeclaration()
            instruction = mem.getInstructionFromDeclaration(declaration)
            mem.addToPending(instruction)

    def setup(self):
        self.orderPendingInstructions()

    def run(self):
        num_instances = len(self.run_instances)
        for i in range(num_instances):
            instance = self.run_instances.pop(0)
            instance.run_all()
        # print("num instances: ", len(self.run_instances))
        # for runner_instance in self.run_instances:
            # runner_instance.run_all()

