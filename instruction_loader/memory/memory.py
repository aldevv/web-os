from .declaration_structure import Declarable_item


class Memory:
    def __init__(self, memory_available, kernel, acumulador):
        self.initial_memory   = memory_available - kernel
        self.memory_available = memory_available - kernel - 1  # acumulador
        self.memory_slots     = []  # secuencia que guarda cada instruccion en respectiva posicion secuencial
        self.acumulador       = acumulador
        self.variables        = Declarable_item()
        self.tags             = Declarable_item()
        self.memory_slots.append("acumulador")

    def print_all_declarations(self):
        print(f"0: acumulador = {self.getAcumulador()}")
        for i, name in enumerate(self.variables.all_data_names):
            print(f"{i+1}: {name} = {self.variables.all_data[name]} ")

    def getAcumulador(self):
        return self.acumulador

    def setAcumulador(self, value):
        self.acumulador = value

    def inDeclarations(self, name):
        if name in self.variables.all_data:
            return True
        else:
            return False

    def getVariable(self, name):
        return self.variables.all_data[name]

    def setVariable(self, name, value, tag=False):
        self.include_in_declarations(value, name)
        self.validate_in_declaration_name_list(name)
        self.append_to_variables_or_tags_list(name, tag)

    def include_in_declarations(self, value, name):
        self.variables.all_data[name] = value

    def validate_in_declaration_name_list(self, name):
        if name not in self.get_declaration_name_list():
            self.reduce_memory_by_1()
            self.include_in_declaration_name_list(name)

    def get_declaration_name_list(self):
        return self.variables.all_data_names

    def reduce_memory_by_1(self):
        self.memory_available -= 1

    def include_in_declaration_name_list(self, name):
        self.variables.all_data_names.append(name)

    def append_to_variables_or_tags_list(self, name, tag):
        if tag == False:
            self.variables.data.append(name)
        else:
            self.tags.data.append(name)

    def save_instruction_to_memory(self, instruction):
        self.add_to_memory_slot(instruction)
        self.reduce_memory_by_1()

    def add_to_memory_slot(self, instruction):
        # saves the command int a slot so it can be loaded later with vaya (goto)
        self.memory_slots.append(instruction)

    def access_memory(self, id_):
        return self.memory_slots[id_]

    def instructions_loaded(self):
        return self.memory_slots

    def num_instructions_loaded(self):
        return len(self.memory_slots)  # because acumulador is not counted

    def get_available_memory(self):
        return self.memory_available

    def memory_isEmpty(self):
        return self.memory_available == 0

    def get_used_memory(self):
        return self.initial_memory - self.memory_available

    def getVariables(self):
        return self.variables.data

    def getTags(self):
        return self.tags.data
