from ..errorHandling          import ErrorHandlerCompiler
from ..factory               import Factory
import os.path

class Compiler:
    def __init__(self, mem, progDefs):
        self.mem                   = mem
        self.progDefs              = progDefs
        self.current_line          = None
        self.programLength         = []
        self.program_history       = []

    def compileFile(self, path):
        self.current_line = self.startPosition()
        lines = self.parseFile(path)
        self.programLength.append(len(lines))
        try:
            for line in lines:
                if self.isComment(line):
                    continue
                self.parse_and_compile_line(line)
                self.nextPosition()
        except Exception as err:
            print("Hubo un error y no se puede continuar", err.args, "line " + str(self.current_line))
    
    def startPosition(self):
        self.mem.setMemoryBeforeCompile()
        return self.mem.num_instructions_saved()

    def parseFile(self, path):
        with open(path) as f:
            lines = [line.rstrip() for line in f if line not in ['\n', '\r\n']]
        return lines

    def isComment(self,string):
        return True if string[0] == "#" or string[:2] == "//" else False

    def parse_and_compile_line(self, string):
        string = string.split()
        self.compile_(string)
    
    def nextPosition(self):
        self.current_line += 1

    def compile_(self,string):
        if self.mem.memory_isEmpty():
            ErrorHandlerCompiler.throw_not_enough_memory_comp(string)
            raise Exception("Memoria")
                
        self.mem.save_instruction_to_memory(string)
        self.validate_and_save(string)

    def validate_and_save(self, instruction):
        declaration_name = self.program_name(instruction)
        if declaration_name in self.progDefs.get_possible_declarations():
            self.run_declaration(declaration_name, instruction)
            self.save_in_history(instruction)

    def program_name(self, instruction):
        return instruction[0]

    def run_declaration(self, name, instruction):
        try:
            self.progDefs.get_possible_declarations()[name](*instruction[1:])
        except TypeError:
            ErrorHandlerCompiler.throw_too_many_arguments(name, instruction)
            raise

    def save_in_history(self, instruction):
        self.program_history.append((self.current_line, instruction))
    
    def get_program_history(self):
        return self.program_history

    def num_prog_compiled(self):
        return len(self.program_history)
    
    def getProgramLength(self):
        return self.programLength

if __name__ == "__main__":
    #! TODO
    """
    imprima
    """ 
