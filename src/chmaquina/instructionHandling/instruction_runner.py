from ..errorHandling          import ErrorHandlerCompiler, ErrorHandlerVariables
from ..factory               import Factory

class InstructionRunner:
    def __init__(self, mem, variables, tags):
        self.__mem     = mem
        self.progDefs  = Factory.createProgramDefinitions(mem, variables, tags, self)
        self.index     = 1 # represents the current instruction
        self.stdin     = []
        self.possible_operators = { 
                        "cargue":       self.progDefs.cargar, 
                        "almacene":     self.progDefs.almacene,
                        "vaya":         self.progDefs.vaya, 
                        "vayasi":       self.progDefs.vayasi,
                        "lea":          self.progDefs.lea,
                        "sume":         self.progDefs.sume,
                        "reste":        self.progDefs.reste,
                        "multiplique":  self.progDefs.multiplique,
                        "divida":       self.progDefs.divida,
                        "potencia":     self.progDefs.potencia,
                        "modulo":       self.progDefs.modulo,
                        "concatene":    self.progDefs.concatene,
                        "elimine":      self.progDefs.elimine,
                        "extraiga":     self.progDefs.extraiga,
                        "Y":            self.progDefs.Y,
                        "O":            self.progDefs.O,
                        "NO":           self.progDefs.NO,
                        "muestre":      self.progDefs.muestre,
                        "imprima":      self.progDefs.imprima,
                        "max":          self.progDefs.max_,
                        "returne":      self.progDefs.returne
        }

    def run_all(self):
        if self.__mem.memory_isEmpty():
            ErrorHandlerCompiler.throw_not_enough_memory_runtime()
            return
        self.run_saved_instructions()

    def run_saved_instructions(self):
        while self.getIndex() < self.__mem.num_instructions_saved():
            self.load_instruction(self.index)
            self.nextPosition()

    def getIndex(self):
        return self.index

    def load_instruction(self, id_):
        instruction = self.__mem.access_memory(id_)
        # print(instruction) 
        operator = self.program_name(instruction)
        if operator in self.possible_operators:
            self.run_operator(operator, instruction)

    def program_name(self, instruction):
        return instruction[0]


    def nextPosition(self):
        self.index += 1

    def run_operator(self, name, instruction):
        try:
            self.possible_operators[name](*instruction[1:])
        except TypeError:
            ErrorHandlerCompiler.throw_too_many_arguments(name, instruction)

    def setIndex(self, value):
        self.index = value

    def appendStdin(self, string):
        self.stdin.append(string)
    
    def getStdin(self):
        return self.stdin