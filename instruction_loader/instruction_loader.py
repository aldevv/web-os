from .memory import Memory
from .programImp import Program
from .errorHandlerCompiler import ErrorHandlerCompiler

class Instruction_loader:
    def __init__(self,memory_available=80,kernel=10, acumulador=0):
        self.mem   = Memory(memory_available,kernel,acumulador)
        self.prog  = Program(self.mem)
        self.e     = ErrorHandlerCompiler()
        self.index = 1 # represents the current instruction
        self.possible_operators = { # todos definidos en Program
                        "cargue":self.prog.cargar, 
                        "almacene":self.prog.almacene,
                        "vaya":self.vaya, 
                        "vayasi":self.vayasi,
                        "lea":self.prog.lea,
                        "sume":self.prog.sume,
                        "reste":self.prog.reste,
                        "multiplique":self.prog.multiplique,
                        "divida":self.prog.divida,
                        "potencia":self.prog.potencia,
                        "modulo":self.prog.modulo,
                        "concatene":self.prog.concatene,
                        "elimine":self.prog.elimine,
                        "extraiga":self.prog.extraiga,
                        "Y":self.prog.Y,
                        "O":self.prog.O,
                        "NO":self.prog.NO,
                        "muestre":self.prog.muestre,
                        "imprima":self.prog.imprima,
                        "max":self.prog.max_,
                        "returne":self.prog.returne
        }

        self.possible_declarations = {
                        "nueva":self.prog.nueva,
                        "etiqueta":self.prog.etiqueta,
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
            self.e.throw_not_enough_memory_comp(string)
            return
        self.mem.save_instruction_to_memory(string)
        self.validate_and_save(string)


    def validate_and_save(self, instruction):
        declaration = self.operator_or_declaration_name(instruction)
        if declaration in self.possible_declarations:
            self.exec_instruction(declaration, instruction)

    def operator_or_declaration_name(self, instruction):
        return instruction[0]

    def exec_instruction(self, name, instruction, declaration=True):
        try:
            if(declaration):
                self.possible_declarations[name](*instruction[1:])
            else:
                self.possible_operators[name](*instruction[1:])
        except TypeError:
            self.e.throw_too_many_arguments()

    def run_instruction(self, id_):
        instruction = self.mem.access_memory(id_)
        # print(instruction) 
        operator = self.operator_or_declaration_name(instruction)
        if operator in self.possible_operators:
            self.exec_instruction(operator, instruction,declaration=False)

    def run_all(self):
        if self.mem.memory_isEmpty():
            self.e.throw_not_enough_memory_runtime()
            return
        self.run_instructions_in_memory()


    def run_instructions_in_memory(self):
        while self.getIndex() < self.mem.num_instructions_loaded():
            self.run_instruction(self.index)
            self.nextPosition()

    def nextPosition(self):
        self.index += 1

    def getIndex(self):
        return self.index

    def vaya(self,tag):
        if not self.mem.inDeclarations(tag):
            self.prog.e.throw_tag_no_declarada(tag)
            return
        self.index = self.mem.getVariable(tag) -1 # makes it equal to the value in tag1


    def vayasi(self, tag1, tag2):
        if not self.mem.inDeclarations(tag1):
            self.prog.e.throw_tag_no_declarada(tag1)
            exit()
            return
        if not self.mem.inDeclarations(tag2):
            self.prog.e.throw_tag_no_declarada(tag2)
            exit()
            return
        if self.mem.getAcumulador() > 0:
            self.index = self.mem.getVariable(tag1) -1 # makes it equal to the value in tag1
            return
        if self.mem.getAcumulador() < 0:
            self.index = self.mem.getVariable(tag2)-1 # makes it equal to the value in tag2
            return

    def debug_run(self):
            print("___________________-")
            print(f"instruccion: {self.index}")
            print("___________________-")
            print(self.mem.access_memory(self.index))
            self.mem.print_all_declarations()
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
    mivariable = myinstructions.mem.getVariable("mivariable")
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
