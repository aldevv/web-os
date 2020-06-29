from ..memory              import Memory
from ..declaration         import Declaration, Declarable_Item
from ..program_definitions import DeclarationDefinitions, OperatorDefinitions

class Factory:
    @staticmethod
    def createCompiler(mem, declaration):
        from ..instructionHandling   import Compiler
        compiler = Compiler(mem)
        compiler.setProgdefs(Factory.createDeclarationDefinitions(mem, declaration))
        return compiler


    @staticmethod
    def createInstructionRunner(mem, declaration):
        from ..instructionHandling   import InstructionRunner
        runner = InstructionRunner(mem)
        runner.setProgdefs(Factory.createOperatorDefinitions(mem, declaration, runner))
        return runner

    @staticmethod
    def createMemory(memory_available,kernel):
        return Memory(memory_available,kernel)

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
