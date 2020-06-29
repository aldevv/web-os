from ..errorHandling          import ErrorHandlerCompiler
from ..factory               import Factory
import os.path

class Compiler:
    def __init__(self, mem, progDefs):
        self.mem                   = mem
        self.progDefs              = progDefs
        self.current_line          = None
        self.programLength         = []
        self.declarations_executed_history       = []
        self.currentProgram        = []

    def compileLines(self, lines):
        self.current_line = len(lines)
        self.mem.setMemoryBeforeCompile()
        for instruction in lines:
            self.parse_and_compile_line(instruction)
        self.mem.saveProgram(self.currentProgram)
        # print("before run programs saved:",self.mem.programs_saved)

    def compileFile(self, path):
        self.mem.setMemoryBeforeCompile()
        self.mem.fileInfo.saveFilePath(path)
        self.current_line = self.startPosition()
        lines = self.parseFile(path)
        try:
            for line in lines:
                if self.isComment(line):
                    continue
                self.parse_and_compile_line(line)
                self.nextPosition()
            self.mem.saveProgram(self.currentProgram)
            self.programLength.append(len(self.currentProgram))
            self.currentProgram = []
        except Exception as err:
            print("Hubo un error y no se puede continuar(compilador)", err.args, "line " + str(self.current_line))
    
    def startPosition(self):
        last = -1
        return self.mem.num_instructions_saved(last)

    def parseFile(self, path):
        with open(path) as f:
            lines = [line.rstrip() for line in f if line not in ['\n', '\r\n']]
        return lines

    def isComment(self,string):
        return True if string[0] == "#" or string[:2] == "//" else False

    def parse_and_compile_line(self, string):
        if self.mem.memory_isEmpty():
            ErrorHandlerCompiler.throw_not_enough_memory_comp(string)
            raise Exception("Memoria")

        string = string.split()
        self.currentProgram.append(string)
        self.compile_(string)
    
    def nextPosition(self):
        self.current_line += 1

    def compile_(self,string):
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
        if self.current_line != None:
            self.declarations_executed_history.append((self.current_line, instruction))
    
    def get_declarations_executed_history(self):
        return self.declarations_executed_history

    def num_prog_compiled(self):
        return len(self.declarations_executed_history)
    
    def getProgramLengthNoComments(self):
        return self.programLength

if __name__ == "__main__":
    #! TODO
    """
    imprima
    """ 
