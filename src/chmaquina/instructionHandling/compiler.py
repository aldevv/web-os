from ..errorHandling          import ErrorHandlerCompiler
from ..factory               import Factory
import os.path

class Compiler:
    def __init__(self, mem, variables, tags):
        self.mem = mem
        self.progDefs  = Factory.createProgramDefinitions(mem, variables, tags)
        self.possible_declarations = {
                        "nueva":self.progDefs.nueva,
                        "etiqueta":self.progDefs.etiqueta,
        }

    def compileFile(self, path):
        lines = self.parseFile(path)
        try:
            for line in lines:
                self.parse_and_compile_line(line)
        except Exception as err:
            print("Hubo un error y no se puede continuar", err.args)

    def parseFile(self, path):
        # path = os.path.dirname(__file__) + '/../../../' + path
        with open(path) as f:
            lines = [line.rstrip() for line in f]
        return lines

    def parse_and_compile_line(self, string):
        if self.isComment(string):
            return
        string = string.split()
        self.compile_(string)
    
    def isComment(self,string):
        return True if string[0] == "#" else False

    def compile_(self,string):
        if self.mem.memory_isEmpty():
            ErrorHandlerCompiler.throw_not_enough_memory_comp(string)
            raise Exception("Memoria")
                
        self.mem.save_instruction_to_memory(string)
        self.validate_and_save(string)


    def validate_and_save(self, instruction):
        declaration = self.program_name(instruction)
        if declaration in self.possible_declarations:
            self.run_declaration(declaration, instruction)


    def run_declaration(self, name, instruction):
        try:
            self.possible_declarations[name](*instruction[1:])
        except TypeError:
            ErrorHandlerCompiler.throw_too_many_arguments(name, instruction)
            raise

    def program_name(self, instruction):
        return instruction[0]

if __name__ == "__main__":
    #! TODO
    """
    imprima
    """ 
