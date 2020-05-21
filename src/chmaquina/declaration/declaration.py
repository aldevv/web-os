from .declarable_item import Declarable_Item

class Declaration:
    def __init__(self, memory):
        self.variables = Declarable_Item(memory)
        self.tags      = Declarable_Item(memory)
    
    def inDeclarations(self, name):
        return True if self.variables.inDeclarations(name) == True or self.tags.inDeclarations(name) == True else False

    def getVariable(self, name):
        return self.variables.getValue(name)
    
    def setVariable(self, name, value):
        self.variables.setValue(name, value)

    def getTag(self, name):
        return self.tags.getValue(name)

    def setTag(self, name, value):
        self.tags.setValue(name, value)
    
    def getVariables(self):
        return self.variables.getNames()

    def getTags(self):
        return self.tags.getNames()
    
    def getVariableType(self, name):
        return self.variables.getType(name)
    
    def getAllNames(self):
        return self.variables.getNames() + self.tags.getNames()
    
    def clear(self):
        self.variables.clearData()
        self.tags.clearData()