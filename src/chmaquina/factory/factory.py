from ..memory              import Memory
from ..declaration         import Declaration, Declarable_Item
from ..program_definitions import DeclarationDefinitions, OperatorDefinitions
from ..scheduler           import Scheduler

class Factory:
    @staticmethod
    def createCompiler(mem, declaration):
        from ..instructionHandling   import Compiler
        return Compiler(mem, Factory.createDeclarationDefinitions(mem, declaration))

    @staticmethod
    def createInstructionRunner(mem, declaration):
        from ..instructionHandling   import InstructionRunner
        runner = InstructionRunner(mem)
        runner.setProgdefs(Factory.createOperatorDefinitions(mem, declaration, runner))
        return runner

    @staticmethod
    def createMemory(memory_available,kernel,acumulador):
        return Memory(memory_available,kernel,acumulador)

    @staticmethod
    def createDeclaration(mem):
        return Declaration(mem)
    
    @staticmethod
    def createDeclarable(mem):
        return Declarable_Item(mem)

    @staticmethod
    def createDeclarationDefinitions(mem, declaration):
        return DeclarationDefinitions(mem, declaration)

    @staticmethod
    def createOperatorDefinitions(mem, declaration, runner):
        return OperatorDefinitions(mem, declaration, runner)

    @staticmethod
    def createScheduler():
        return Scheduler()
