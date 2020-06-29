class Declarable_Item :
    def __init__(self, memory):
        self.all_data = {}
        self.__mem = memory
        self.types = {} 
    
    def print_all_declarations(self):
        print(f"0: acumulador = {self.__mem.getAcumulador()}")
        for i, name in enumerate(self.all_data):
            print(f"{i+1}: {name} = {self.all_data[name]} ")

    def getValue(self, name):
        return self.all_data[name]

    def getType(self, name):
        return self.types[name]

    def inDeclarations(self, name):
        return True if name in self.all_data else False

    def setValue(self, name, value):
        self.save_type_and_use_memory_if_first_time(name, value)
        self.update_value_in_declarations(name, value)
    
    def save_type_and_use_memory_if_first_time(self, name, value):
        if not self.inDeclarations(name):
            self.types[name] = type(value)

    def update_value_in_declarations(self, name, value):
        if type(value) == self.types[name]:
            self.all_data[name] = value
        else:
            print("wrong type!")

    def getMemory(self):
        return self.__mem
    
    def getNames(self):
        return list(self.all_data.keys())
    
    def clearData(self):
        self.all_data.clear()