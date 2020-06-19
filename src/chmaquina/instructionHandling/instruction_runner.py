from ..errorHandling          import ErrorHandlerCompiler, ErrorHandlerVariables
from ..factory               import Factory
import traceback

class InstructionRunner:
    def __init__(self, mem):
        self.__mem              = mem
        self.progDefs           = None
        self.current_line       = None # represents the current instruction
        self.stdout             = []
        self.printer            = []
        self.operators_executed_history    = []

    def getMemory(self):
        return self.__mem

    def run_line(self):
        programs_to_run = self.__mem.pending_programs
        if len(programs_to_run) == 0:
                print("nothing more to run")
                return
        
        # print("current Line", self.getCurrentLine())
        # print("num Instruct", len(programs_to_run[0])-1)

        instruction = self.find_instruction(programs_to_run, self.current_line)
        self.load_instruction(programs_to_run)
        self.nextPosition()
        if self.getCurrentLine() == len(programs_to_run[0]):
            programs_to_run.pop(0)
            self.current_line = None
        print("instruction: ", instruction)
        # print("pending_ programs", programs_to_run)
        print("step", self.__mem.getSteps())
        print("\n____________\n")
        if instruction[0] in self.progDefs.possible_operators:
            return True
        else:
            return False

    def run_all(self, ):
        self.setStartPosition()
        self.run_saved_instructions()
    
    def setStartPosition(self):
        self.current_line = self.__mem.getMemoryBeforeCompile()

    def run_saved_instructions(self):
        try:
            programs_to_run = self.__mem.pending_programs
            while self.getCurrentLine() < len(programs_to_run[0]):
                self.load_instruction(programs_to_run)
                self.nextPosition()
            programs_to_run.pop(0)
            self.__mem.saveDeclaration(self.progDefs.getDeclaration(), True)
        except Exception as err:
            print(traceback.format_exc())
            print("Hubo un error en runtime ", err.args, self.getCurrentLine(), err)

    def getCurrentLine(self):
        return self.current_line

    def load_instruction(self, programs_to_run):
        instruction = self.find_instruction(programs_to_run, self.getCurrentLine())
        operator = self.program_name(instruction)
        if operator in self.progDefs.get_possible_operators():
            self.run_operator(operator, instruction)
            self.save_in_history(instruction)

    def find_instruction(self, programs_to_run, id_):
        return programs_to_run[0][id_]

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
        self.operators_executed_history.append((self.current_line+1, instruction))

    def setLine(self, value):
        self.current_line = value

    def appendStdout(self, string):
        self.stdout.append(string)
    
    def appendPrinter(self, string):
        self.printer.append(string)

    def getPrinter(self):
        return self.printer

    def getStdout(self):
        return self.stdout

    def get_operators_executed_history(self):
        return self.operators_executed_history

    def num_prog_ran(self):
        return len(self.operators_executed_history)

    def setProgdefs(self, progDefs):
        self.progDefs = progDefs