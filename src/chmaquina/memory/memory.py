

class Memory:
    def __init__(self, memory_available, kernel, acumulador):
        self.kernel           = kernel
        self.initial_memory   = memory_available
        self.memory_available = memory_available - kernel - 1 # del acumulador 
        self.pre_compile_memory   = 0
        self.memory_programs  = []  # secuencia que guarda cada instruccion en respectiva posicion secuencial
        self.acumulador       = acumulador
        self.step_by_step     = []
        self.memory_programs.append(["acumulador"])

    def get_used_memory(self):
        return self.initial_memory - self.memory_available

    def get_available_memory(self):
        return self.memory_available

    def saveProgram(self, program):
        self.appendProgram(program)

    def appendProgram(self, program):
        # saves the command int a slot so it can be loaded later with vaya (goto)
        self.memory_programs.append(program)

    def reduce_memory_by_1(self):
        self.memory_available -= 1

    def memory_isEmpty(self):
        return self.memory_available <= 0

    def find_instruction(self, id_):
        return self.memory_programs[-1][id_]

    def programs_saved(self): # change to programs saved
        return self.memory_programs[1:]

    def num_instructions_saved(self):
        return len(self.memory_programs[-1])

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
        if len(self.memory_programs) == 1:
            self.pre_compile_memory = 0
        else:
            sum_ = 0
            for program in self.memory_programs:
                sum_ += len(program)
            return sum_-1 # because acu

    def getMemoryBeforeCompile(self):
        return self.pre_compile_memory
    



