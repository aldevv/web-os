
class MachinaSettings:
    def __init__(self, memory_available ,kernel):
        self.kernel             = kernel
        self.acumulador         = {}
        self.initial_memory     = memory_available #! do i need this?
        self.pre_compile_memory = 0
        self.program_last_run   = None
     
    def getPreCompileMemory(self):
         return self.pre_compile_memory
    
    def setPreCompileMemory(self, value):
        self.pre_compile_memory = value

    def getKernel(self):
        return self.kernel

    def getAcumulador(self, declaration):
        if declaration not in self.acumulador:
            return 0
        return self.acumulador[declaration]

    def setAcumulador(self, declaration, value):
        self.acumulador[declaration] = value

    def getInitialMemory(self):
        return self.initial_memory

    def getAcumuladorLastRun(self):
        if self.program_last_run == None:
            return 0
        declaration = self.program_last_run.progDefs.getDeclaration()
        return self.acumulador[declaration]

    def saveInstanceAsLastRun(self, instance):
        self.program_last_run = instance
        declaration = instance.progDefs.getDeclaration()
        if declaration not in self.acumulador:
            self.acumulador[declaration] = 0
    
    def getProgramLastRun(self):
        return self.program_last_run