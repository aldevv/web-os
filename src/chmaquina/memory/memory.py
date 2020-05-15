

class Memory:
    def __init__(self, memory_available, kernel, acumulador):
        self.initial_memory   = memory_available - kernel
        self.memory_available = memory_available - kernel - 1  # acumulador
        self.memory_slots     = []  # secuencia que guarda cada instruccion en respectiva posicion secuencial
        self.acumulador       = acumulador
        self.memory_slots.append("acumulador")

    def get_used_memory(self):
        return self.initial_memory - self.memory_available

    def get_available_memory(self):
        return self.memory_available

    def getAcumulador(self):
        return self.acumulador

    def setAcumulador(self, value):
        self.acumulador = value

    def reduce_memory_by_1(self):
        self.memory_available -= 1

    def save_instruction_to_memory(self, instruction):
        self.add_to_memory_slot(instruction)
        self.reduce_memory_by_1()

    def add_to_memory_slot(self, instruction):
        # saves the command int a slot so it can be loaded later with vaya (goto)
        self.memory_slots.append(instruction)

    def access_memory(self, id_):
        return self.memory_slots[id_]

    def instructions_saved(self):
        return self.memory_slots

    def num_instructions_saved(self):
        return len(self.memory_slots)  # because acumulador is not counted


    def memory_isEmpty(self):
        return self.memory_available <= 0

