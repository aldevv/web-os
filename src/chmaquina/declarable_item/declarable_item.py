class Declarable_Item :
    all_data = {}
    all_data_names = []
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
        # self.check_and_save_step(name, value)
        self.update_value_in_declarations(value, name)
        self.validate_in_declaration_name_list(name)

    def check_and_save_step(self, name, new_value):
        if(name in Declarable_Item.all_data):
            self.__mem.saveStep(name, Declarable_Item.all_data[name], new_value)
        else:
            self.__mem.saveStep(name, "create", new_value)

    def update_value_in_declarations(self, value, name):
        Declarable_Item.all_data[name] = value

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