from ..memory                import Memory
from ..declarable_item       import Declarable_Item
from ..program_definitions   import ProgramDefinitions

class Factory:
    @staticmethod
    def createCompiler(mem, variables, tags):
        from ..instructionHandling   import Compiler
        return Compiler(mem, variables, tags)

    @staticmethod
    def createInstructionRunner(mem, variables, tags):
        from ..instructionHandling   import InstructionRunner
        return InstructionRunner(mem, variables, tags)

    @staticmethod
    def createMemory(memory_available,kernel,acumulador):
        return Memory(memory_available,kernel,acumulador)
    
    @staticmethod
    def createDeclarable(mem):
        return Declarable_Item(mem)

    @staticmethod
    def createProgramDefinitions(mem, variables, tags, runner=None):
        return ProgramDefinitions(mem, variables, tags, runner)


