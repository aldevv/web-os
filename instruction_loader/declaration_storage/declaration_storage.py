class Declarable_Item :
    all_data = {}
    all_data_names = []
    def __init__(self, memory):
        self.__names =  []
        self.__mem = memory
    
    def getMemory(self):
        return self.__mem

    def print_all_declarations(self):
        print(f"0: acumulador = {self.__mem.getAcumulador()}")
        for i, name in enumerate(Declarable_Item.all_data_names):
            print(f"{i+1}: {name} = {Declarable_Item.all_data[name]} ")

    def inDeclarations(self, name):
        if name in Declarable_Item.all_data:
            return True
        else:
            return False

    def getVariable(self, name):
        return Declarable_Item.all_data[name]

    def setVariable(self, name, value, tag=False):
        self.update_value_in_declarations(value, name)
        self.validate_in_declaration_name_list(name)
        self.append_name(name)

    def update_value_in_declarations(self, value, name):
        Declarable_Item.all_data[name] = value

    def validate_in_declaration_name_list(self, name):
        if name not in self.get_declaration_name_list():
            self.__mem.reduce_memory_by_1()
            self.include_in_declaration_name_list(name)

    def append_name(self, name):
        self.__names.append(name)

    def get_declaration_name_list(self):
        return Declarable_Item.all_data_names

    def include_in_declaration_name_list(self, name):
        Declarable_Item.all_data_names.append(name)

    def getNames(self):
        return self.__names