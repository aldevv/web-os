

class Memory:
    def __init__(self, memory_available, kernel, acumulador):
        self.all = self.set_all(kernel)
        self.kernel           = kernel
        self.acumulador       = acumulador
        self.initial_memory   = memory_available
        self.memory_available = memory_available - kernel - 1 # del acumulador 
        self.pre_compile_memory   = 0
        self.programs_saved  = []  
        self.declarationHistory = {} # could be a list
        self.declarationHash = {}
        self.step_by_step     = []

    def set_all(self, kernel):
        return [["Acumulador"]] + [["OS " + str(i)] for i in range(kernel)]
    
    def get_all(self):
        return self.all

    def saveDeclaration(self, declaration, update=None):
        if update == True:
            last_element = len(self.declarationHistory) - 1
            self.declarationHistory[last_element] = declaration
        else:
            self.declarationHistory[len(self.declarationHistory)] = declaration
            self.saveDeclarationsInstruction(declaration)

    def saveDeclarationsInstruction(self, declaration):
        self.declarationHash[declaration] = self.get_programs()[-1]

    def getVariables(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getVariables())
        return all_
        
    def getTags(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getTags())
        return all_

    def getDeclarationHistory(self):
        return self.declarationHistory

    def getInstructionFromDeclaration(self, declaration):
        return self.declarationHash[declaration]

    def get_used_memory(self):
        return self.initial_memory - self.memory_available

    def get_available_memory(self):
        return self.memory_available

    def saveProgram(self, program):
        self.appendProgram(program)

    def appendProgram(self, program):
        # saves the command int a slot so it can be loaded later with vaya (goto)
        self.programs_saved.append(program)

    def reduce_memory_by_1(self):
        self.memory_available -= 1

    def memory_isEmpty(self):
        return self.memory_available <= 0

    def find_instruction(self, id_):
        return self.programs_saved[-1][id_]

    def get_programs(self): # change to programs saved
        # return self.programs_saved[1:]
        return self.programs_saved

    def num_instructions_saved(self):
        return len(self.programs_saved[-1]) if len(self.programs_saved) != 0 else 0

    def getAcumulador(self):
        return self.acumulador

    def setAcumulador(self, value):
        self.acumulador = value

    def saveStepOneArg(self, name, old_value, new_value=None):
        if new_value != None:
            step = str(name) + ": "+ str(old_value) + " => " + str(new_value)
        else:
            step = str(name) + ": "+ str(old_value) 
        self.append_step(step)
    
    def saveStepTwoArg(self, func_name, first, second, ans):
        step = str(first) + " " + str(func_name) + " " + str(second) + " => " + str(ans)
        self.append_step(step)

    def append_step(self, step):
        self.step_by_step.append(step)

    def getSteps(self):
        return self.step_by_step
    
    def getKernel(self):
        return self.kernel
    
    def setMemoryBeforeCompile(self):
        #used so that the runner knows where the program saved starts
        if len(self.programs_saved) == 0:
            self.pre_compile_memory = 0
        else:
            sum_ = 0
            for program in self.programs_saved:
                sum_ += len(program)
            return sum_-1 # because acu

    def getMemoryBeforeCompile(self):
        return self.pre_compile_memory
    



