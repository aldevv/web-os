
class DeclarationHistory:

    def __init__(self, memory):
        self.mem = memory
        self.os_memory = None
        self.declarationHistory = {}
        self.declarationHashInstruction = {}
        self.expropiativeDeclarationHashInstruction = {}
        self.pending_declarations = []

    

    def getMemory(self): 
        memory = self.get_all()
        declarationHistory = self.getDeclarationHistory()
        for id_ in declarationHistory:
            memory += self.getInstructionFromDeclaration(declarationHistory[id_])
            variables = declarationHistory[id_].getVariables()
            tags      = declarationHistory[id_].getTags()
            memory += [[declarationHistory[id_].getVariable(var)] for var in variables]
            memory += [[declarationHistory[id_].getTag(tag)] for tag in tags]

        numElements = len(memory)
        current = 0
        for i in range(numElements):
            memory[current] = (i, memory[current])
            current += 1
        return memory

    def get_all(self):
        self.os_memory = self.set_all(self.mem.getKernel())
        return self.os_memory

    def set_all(self, kernel):
        return [[self.mem.getAcumuladorLastRun()]] + [["OS " + str(i)] for i in range(kernel)]

    def getVariables(self):
        memory = self.get_all()
        declarationHistory = self.getDeclarationHistory()
        all_vars = []
        for id_ in declarationHistory:
            memory += self.getInstructionFromDeclaration(declarationHistory[id_])
            numElements = len(memory)
            variables = declarationHistory[id_].getVariables()
            tags      = declarationHistory[id_].getTags()
            indexLimit = numElements + len(variables)
            current = 0
            varNoPos = variables.copy()

            for i in range(numElements, indexLimit):
                variables[current] = (i, variables[current])
                current +=1
            all_vars.append(variables)
            memory += [[declarationHistory[id_].getVariable(var)] for var in varNoPos]
            memory += [[declarationHistory[id_].getTag(tag)] for tag in tags]
        return all_vars

    def getTags(self):
        memory = self.get_all()
        declarationHistory = self.getDeclarationHistory()
        all_tags = []
        for id_ in declarationHistory:
            memory += self.getInstructionFromDeclaration(declarationHistory[id_])
            variables = declarationHistory[id_].getVariables()
            tags = declarationHistory[id_].getTags()
            memory += [[declarationHistory[id_].getVariable(var)] for var in variables]
            numElements = len(memory)
            indexLimit = numElements + len(tags)
            current = 0
            tagsNoPos = tags.copy()
            for i in range(numElements, indexLimit):
                tags[current] = (i, tags[current])
                current +=1
            all_tags.append(tags)
            memory += [[declarationHistory[id_].getTag(tag)] for tag in tagsNoPos]
        return all_tags

    def saveDeclaration(self, declaration, update):
        if update == True:
            last_element = len(self.declarationHistory) - 1
            self.declarationHistory[last_element] = declaration
        else:
            self.declarationHistory[len(self.declarationHistory)] = declaration
            self.saveDeclarationsInstruction(declaration)

    def addStatusAsNotComplete(self, declaration):
        self.mem.getDataStream().appendStatus(declaration, 1)

    def saveDeclarationsInstruction(self, declaration):
        self.declarationHashInstruction[declaration] = self.mem.get_programs()[-1]

    def getVariablesNoPos(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getVariables())
        return all_
        
    def getTagsNoPos(self):
        all_ = []
        for id_ in self.declarationHistory:
            all_.append(self.declarationHistory[id_].getTags())
        return all_

    def getDeclarationHistory(self):
        return self.declarationHistory

    def setDeclarationHistory(self, something):
        self.declarationHistory = something

    def getInstructionFromDeclaration(self, declaration):
        return self.declarationHashInstruction[declaration]

    def addToPending(self, declaration):
        self.pending_declarations.append(declaration)
    
    def getPending(self):
        return self.pending_declarations

    def saveDeclarationsInstructionExpropiative(self, declaration, instruction):
        self.expropiativeDeclarationHashInstruction[declaration] = instruction