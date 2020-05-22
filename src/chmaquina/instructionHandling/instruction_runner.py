from ..errorHandling          import ErrorHandlerCompiler, ErrorHandlerVariables
from ..factory               import Factory

class InstructionRunner:
    def __init__(self, mem):
        self.__mem              = mem
        self.progDefs           = None
        self.current_line       = None # represents the current instruction
        self.stdout             = []
        self.program_history    = []

    def run_line(self, atStart=True):
        last_history = self.program_history.copy()
        if atStart:
            self.setStartPosition()
        if self.getCurrentLine() >= self.__mem.num_instructions_saved():
            print("nothing more to run")
            return
        instruction = self.__mem.find_instruction(self.current_line)
        print("instruction: ", instruction)
        print("step", self.__mem.getSteps())
        self.load_instruction()
        self.nextPosition()
        changed = self.program_history != last_history
        if changed:
            self.appendStdout(self.program_history[-1])
        return changed

    def run_all(self):
        self.setStartPosition()
        self.run_saved_instructions()
    
    def setStartPosition(self):
        self.current_line = self.__mem.getMemoryBeforeCompile()

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
        if operator in self.progDefs.get_possible_operators():
            self.run_operator(operator, instruction)
            self.save_in_history(instruction)

    def program_name(self, instruction):
        return instruction[0]

    def nextPosition(self):
        self.current_line += 1

    def run_operator(self, name, instruction):
        try:
            self.progDefs.get_possible_operators()[name](*instruction[1:])
        except TypeError:
            ErrorHandlerCompiler.throw_too_many_arguments(name, instruction)
            raise

    def save_in_history(self, instruction):
        # if instruction[0] == "vaya" or instruction[0] == "vayasi":
        #     return
        self.program_history.append((self.current_line+1, instruction))

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

    def setProgdefs(self, progDefs):
        self.progDefs = progDefs