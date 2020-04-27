from .memory                import Memory
from .programImp            import ProgramDefinitions
from .errorHandling         import ErrorHandlerCompiler, ErrorHandlerVariables
from .declaration_storage   import Declarable_Item

class Instruction_loader:
    def __init__(self,memory_available=80,kernel=10, acumulador=0):
        self.index     = 1 # represents the current instruction
        self.mem       = Memory(memory_available,kernel,acumulador)
        self.variables = Declarable_Item(self.mem)
        self.tags      = Declarable_Item(self.mem)
        self.progDefs  = ProgramDefinitions(self.variables, self.tags, self)
        self.possible_declarations = {
                        "nueva":self.progDefs.nueva,
                        "etiqueta":self.progDefs.etiqueta,
        }
        self.possible_operators = { 
                        "cargue":self.progDefs.cargar, 
                        "almacene":self.progDefs.almacene,
                        "vaya":self.progDefs.vaya, 
                        "vayasi":self.progDefs.vayasi,
                        "lea":self.progDefs.lea,
                        "sume":self.progDefs.sume,
                        "reste":self.progDefs.reste,
                        "multiplique":self.progDefs.multiplique,
                        "divida":self.progDefs.divida,
                        "potencia":self.progDefs.potencia,
                        "modulo":self.progDefs.modulo,
                        "concatene":self.progDefs.concatene,
                        "elimine":self.progDefs.elimine,
                        "extraiga":self.progDefs.extraiga,
                        "Y":self.progDefs.Y,
                        "O":self.progDefs.O,
                        "NO":self.progDefs.NO,
                        "muestre":self.progDefs.muestre,
                        "imprima":self.progDefs.imprima,
                        "max":self.progDefs.max_,
                        "returne":self.progDefs.returne
        }


    def parse_and_compile(self,string):
        if self.isComment(string):
            return
        string = string.split()
        self.compile_(string)
    
    def isComment(self,string):
        return True if string[0] == "#" else False

    def compile_(self,string):
        if self.mem.memory_isEmpty():
            ErrorHandlerCompiler.throw_not_enough_memory_comp(string)
            return
        self.mem.save_instruction_to_memory(string)
        self.validate_and_save(string)


    def validate_and_save(self, instruction):
        declaration = self.function_name(instruction)
        if declaration in self.possible_declarations:
            self.run(declaration, instruction)

    def function_name(self, instruction):
        return instruction[0]

    def run(self, name, instruction, declaration=True):
        try:
            if(declaration):
                self.possible_declarations[name](*instruction[1:])
            else:
                self.possible_operators[name](*instruction[1:])
        except TypeError:
            ErrorHandlerCompiler.throw_too_many_arguments(name, instruction, declaration)

    def run_all(self):
        if self.mem.memory_isEmpty():
            ErrorHandlerCompiler.throw_not_enough_memory_runtime()
            return
        self.run_instructions_in_memory()

    def run_instructions_in_memory(self):
        while self.getIndex() < self.mem.num_instructions_loaded():
            self.run_instruction(self.index)
            self.nextPosition()

    def getIndex(self):
        return self.index

    def run_instruction(self, id_):
        instruction = self.mem.access_memory(id_)
        # print(instruction) 
        operator = self.function_name(instruction)
        if operator in self.possible_operators:
            self.run(operator, instruction,declaration=False)

    def nextPosition(self):
        self.index += 1

    def setIndex(self, value):
        self.index = value

    def getVariables(self):
        return self.variables

    def getTags(self):
        return self.tags

    def getMemory(self):
        return self.mem

    def debug_run(self):
            print("___________________-")
            print(f"instruccion: {self.index}")
            print("___________________-")
            print(self.mem.access_memory(self.index))
            self.variables.print_all_declarations()
            print(f"memory: {self.mem.get_available_memory()} ")


if __name__ == "__main__":
    myinstructions = Instruction_loader(memory_available=50,kernel=20,acumulador=10)
    myinstructions.parse_and_compile("nueva mivariable I 0")
    myinstructions.parse_and_compile("almacene mivariable") # mi variable becomes 40
    myinstructions.parse_and_compile("sume mivariable")
    myinstructions.parse_and_compile("sume mivariable")
    myinstructions.parse_and_compile("cargue mivariable")
    myinstructions.parse_and_compile("sume mivariable")
    myinstructions.parse_and_compile("sume mivariable")
    myinstructions.parse_and_compile("nueva unidad I 1")
    # compiles all, then you run each instruction
    # myinstructions.run_instruction(1)
    # myinstructions.run_instruction(2)
    # myinstructions.run_instruction(3)
    # myinstructions.run_instruction(4)
    # myinstructions.run_instruction(5)
    # myinstructions.run_instruction(6)
    myinstructions.run_all()
    inte = myinstructions.mem.getAcumulador()
    print(f"acumulador {inte}")
    mivariable = myinstructions.variables.getVariable("mivariable")
    print(f"mi variable: {mivariable}")

    #! TODO
    """

    imprima
    select_instruction #! try catch number of arguments!

    first needs to declare all in the file, then ignore those lines and run the rest!
    declarations: nueva, etiqueta

    vaya is gonna need a modification in the memory id_ system because it might repeat instructions that are already loaded

    need to try catch casting errors in nueva

    """ 
