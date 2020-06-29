from .declarationsInMemory import DeclarationHistory
from .files_info           import FileInfo
from .maquina_settings     import MachinaSettings
from .dataStream           import DataStream

class Memory:
    def __init__(self, memory_available, kernel):
        self.settings           = MachinaSettings(memory_available, kernel)
        self.fileInfo           = FileInfo(self)
        self.declarationHistory = DeclarationHistory(self)
        self.dataStream         = DataStream()
        self.pending_programs   = []
        self.programs_saved     = []
        self.step_by_step       = []

    def getDataStream(self):
        return self.dataStream

    def getAcumuladorLastRun(self):
        return self.settings.getAcumuladorLastRun()

    def getMemory(self): 
        return self.declarationHistory.getMemory()

    def getFileInfo(self):
        return self.fileInfo
    
    def orderPendingInstructions(self, run_instances):
        for instance in run_instances:
            declaration = instance.progDefs.getDeclaration()
            instruction = self.getInstructionFromDeclaration(declaration)
            self.addToPending(instruction)

    def orderPendingInstructionsExpro(self, instructions_ready):
        self.pending_programs = instructions_ready

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
        return self.declarationHistory.getInstructionFromDeclaration(declaration)

    def getDeclarationInstructionDictionary(self):
        return self.declarationHistory.declarationHashInstruction

    def get_used_memory(self):
        return len(self.getMemory())

    def get_available_memory(self):
        return self.settings.getInitialMemory()- len(self.getMemory())

    def saveProgram(self, program):
        # saves the command int a slot so it can be loaded later with vaya (goto)
        self.programs_saved.append(program)

    def memory_isEmpty(self):
        return self.settings.getInitialMemory() - len(self.getMemory())<= 0

    def find_instruction(self, program, id_):
        return self.programs_saved[program][id_]

    def get_programs(self): 
        return self.programs_saved

    def num_instructions_saved(self, program):
        return len(self.programs_saved[program]) if len(self.programs_saved) != 0 else 0

    def getAcumulador(self, declaration=None):
        if declaration == None:
            declaration = self.settings.getProgramLastRun().progDefs.getDeclaration()
        return self.settings.getAcumulador(declaration)

    def setAcumulador(self, declaration, value):
        self.settings.setAcumulador(declaration, value)

    def saveInstanceAsLastRun(self, instance):
        self.settings.saveInstanceAsLastRun(instance)

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
        return self.settings.getKernel()
    
    def setMemoryBeforeCompile(self):
        #used so that the runner knows where the program saved starts
        if len(self.programs_saved) == 0:
            self.settings.setPreCompileMemory(0)
        else:
            sum_ = 0
            for program in self.programs_saved:
                sum_ += len(program)
            return sum_-1 # because acu

    def getMemoryBeforeCompile(self):
        return self.settings.getPreCompileMemory()