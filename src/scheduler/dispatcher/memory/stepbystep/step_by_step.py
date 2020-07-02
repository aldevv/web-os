class StepByStep:
    def __init__(self):
        self.step_by_step = {}
        pass


    def getSteps(self, declaration):
        return self.step_by_step[declaration]

    def saveStepOneArg(self,declaration, name, old_value, new_value=None):
        if new_value != None:
            step = str(name) + ": "+ str(old_value) + " => " + str(new_value)
        else:
            step = str(name) + ": "+ str(old_value) 
        self.append_step(declaration, step)

    def append_step(self,declaration, step):
        if declaration not in self.step_by_step:
            steps = []
            steps.append(step)
            self.step_by_step[declaration] = steps
        else: 
            self.step_by_step[declaration].append(step)

    def saveStepTwoArg(self, declaration, func_name, first, second, ans):
        step = str(first) + " " + str(func_name) + " " + str(second) + " => " + str(ans)
        self.append_step(declaration, step)
