from .declarationsInMemory import DeclarationHistory

class Memory:
    def __init__(self, memory_available, kernel, acumulador):
        self.kernel           = kernel
        self.acumulador       = acumulador
        self.initial_memory   = memory_available #! do i need this?
        self.memory_available = memory_available - kernel - 1 #TODO volver len(self.getMemory)
        self.pre_compile_memory = 0
        self.declarationHistory = DeclarationHistory(self)
        self.pending_programs   = []
        self.programs_saved     = []  
        self.step_by_step       = []

    def getMemory(self): 
        return self.declarationHistory.getMemory()

    def getVariables(self): 
        return self.declarationHistory.getVariables()
    
    def addToPending(self, program):
        self.pending_programs.append(program)

    def addDeclarationToPending(self, declaration):
        self.declarationHistory.addToPending(declaration)

    def getPendingDeclarations(self):
        return self.declarationHistory.getPending()

    def getTags(self): 
        return self.declarationHistory.getTags()

    def saveDeclaration(self, declaration, update=None):
        self.declarationHistory.saveDeclaration(declaration, update)

    def getDeclarationHistory(self):
        return self.declarationHistory.getDeclarationHistory()

    def getInstructionFromDeclaration(self, declaration):
        return self.declarationHistory.getInstructionFromDeclaration()

    def get_used_memory(self):
        return self.initial_memory - self.memory_available

    def get_available_memory(self):
        return self.memory_available

    def saveProgram(self, program):
        # saves the command int a slot so it can be loaded later with vaya (goto)
        self.programs_saved.append(program)

    def reduce_memory_by_1(self):
        self.memory_available -= 1

    def memory_isEmpty(self):
        return self.memory_available <= 0

    def find_instruction(self, program, id_):
        return self.programs_saved[program][id_]

    def get_programs(self): 
        return self.programs_saved

    def num_instructions_saved(self, program):
        return len(self.programs_saved[program]) if len(self.programs_saved) != 0 else 0

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
    



