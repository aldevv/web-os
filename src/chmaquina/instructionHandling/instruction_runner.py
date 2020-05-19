from ..errorHandling          import ErrorHandlerCompiler, ErrorHandlerVariables
from ..factory               import Factory

class InstructionRunner:
    def __init__(self, mem, variables, tags):
        self.__mem              = mem
        self.progDefs           = Factory.createProgramDefinitions(mem, variables, tags, self)
        self.current_line       = 1 # represents the current instruction
        self.stdout             = []
        self.program_history    = []
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
        self.run_saved_instructions()

    def run_saved_instructions(self):
        try:
            while self.getCurrentLine() < self.__mem.num_instructions_saved():
                self.load_instruction()
                self.nextPosition()
        except Exception as err:
            print("Hubo un error en runtime ", err.args, self.getCurrentLine())

    def getCurrentLine(self):
        return self.current_line

    def load_instruction(self):
        instruction = self.__mem.find_instruction(self.current_line)
        operator = self.program_name(instruction)
        if operator in self.possible_operators:
            self.run_operator(operator, instruction)
            self.save_in_history(instruction)

    def program_name(self, instruction):
        return instruction[0]

    def nextPosition(self):
        self.current_line += 1

    def run_operator(self, name, instruction):
        try:
            self.possible_operators[name](*instruction[1:])
        except TypeError:
            ErrorHandlerCompiler.throw_too_many_arguments(name, instruction)
            raise

    def save_in_history(self, instruction):
        # if instruction[0] == "vaya" or instruction[0] == "vayasi":
        #     return
        self.program_history.append((self.current_line, instruction))

    def setLine(self, value):
        self.current_line = value

    def appendStdout(self, string):
        self.stdout.append(string)
    
    def getStdout(self):
        return self.stdout

    def get_program_history(self):
        return self.program_history

    def num_prog_ran(self):
        return len(self.program_history)