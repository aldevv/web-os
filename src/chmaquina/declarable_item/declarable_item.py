class Declarable_Item :
    all_data = {}
    all_data_names = []
    types = {} #!TODO check types every time you are gonna set a value
    def __init__(self, memory):
        self.__names =  []
        self.__mem = memory
    
    def print_all_declarations(self):
        print(f"0: acumulador = {self.__mem.getAcumulador()}")
        for i, name in enumerate(Declarable_Item.all_data_names):
            print(f"{i+1}: {name} = {Declarable_Item.all_data[name]} ")

    def inDeclarations(self, name):
        return True if name in Declarable_Item.all_data else False

    def getValue(self, name):
        return Declarable_Item.all_data[name]

    def setValue(self, name, value):
        self.save_type_if_first_time(name, value)
        self.update_value_in_declarations(name, value)
        self.validate_in_declaration_name_list(name)

    def update_value_in_declarations(self, name, value):
        if type(value) == Declarable_Item.types[name]:
            Declarable_Item.all_data[name] = value
        else:
            print("wrong type!")

    def save_type_if_first_time(self, name, value):
        if not self.inDeclarations(name):
            Declarable_Item.types[name] = type(value)

    def validate_in_declaration_name_list(self, name):
        if name not in self.get_all_declaration_names():
            self.__mem.reduce_memory_by_1()
            self.include_in_declaration_name_list(name)
            self.append_name(name)

    def append_name(self, name):
        self.__names.append(name)

    def get_all_declaration_names(self):
        return Declarable_Item.all_data_names

    def include_in_declaration_name_list(self, name):
        Declarable_Item.all_data_names.append(name)
    
    def getMemory(self):
        return self.__mem

    def getNames(self):
        return self.__names
    
    def getAll(self):
        return Declarable_Item.all_data