from .declarationsInMemory import DeclarationHistory
from .files_info           import FileInfo
from .maquina_settings     import MachinaSettings
from .dataStream           import DataStream
from .stepbystep           import StepByStep
from .queues               import Queue

class Memory:
    def __init__(self, memory_available, kernel):
        self.settings           = MachinaSettings(memory_available, kernel)
        self.fileInfo           = FileInfo(self)
        self.declarationHistory = DeclarationHistory(self)
        self.dataStream         = DataStream()
        self.steps              = StepByStep()
        self.queues             = Queue()
        self.programs_saved     = []

    def getDataStream(self):
        return self.dataStream

    def getAcumuladorLastRun(self):
        return self.settings.getAcumuladorLastRun()

    def getMemory(self): 
        return self.declarationHistory.getMemory()

    def getFileInfo(self):
        return self.fileInfo
    
    def getQueues(self):
        return self.queues
    
    def orderPendingInstructions(self, run_instances):
        for instance in run_instances:
            declaration = instance.progDefs.getDeclaration()
            instruction = self.getInstructionFromDeclaration(declaration)
            self.addToPending(instruction)

    def orderPendingInstructionsExpro(self, instructions_ready):
        self.queues.setPendingPrograms(instructions_ready)

    def getVariables(self): 
        return self.declarationHistory.getVariables()
    
    def addToPending(self, program):
        self.queues.addToPending(program)

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

    def saveStepOneArg(self,declaration, name, old_value, new_value=None):
        self.steps.saveStepOneArg(declaration,name,old_value,new_value)
    
    def saveStepTwoArg(self, declaration, func_name, first, second, ans):
        self.steps.saveStepTwoArg(declaration, func_name, first, second, ans)

    def getSteps(self, declaration):
        return self.steps.getSteps(declaration)
    
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