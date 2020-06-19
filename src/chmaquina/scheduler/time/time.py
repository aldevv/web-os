from random import randint
class Time:
    # def __init__(self, slice_=5):
    def __init__(self, slice_=5):
        self.slice       = slice_
        self.IOfunctionExceptions = {'lea', 'imprima', 'muestre'} 

    def calculate_program_time(self, run_instance):
        program = self.getProgramFromInstance(run_instance)
        instructions_with_times = []
        timeOnly                = []
        time = None
        total = 0
        for line in program:
            if line[0] in self.IOfunctionExceptions:
                time = randint(1,9)
            else:
                time = 1
            total += time
        return total

    def getProgramFromInstance(self, instance):
        declaration = instance.progDefs.getDeclaration()
        mem         = instance.getMemory()
        return mem.getInstructionFromDeclaration(declaration)


    def setSlice(self, slice_):
        self.slice = slice_
    
    def getSlice(self):
        return self.slice
    
    def timeLimit(self):
        return self.slice

    def checkIfTheresTime(self, instance):
        program_time = self.calculate_program_time(instance)
        if program_time <=self.slice:
            return True
        return False