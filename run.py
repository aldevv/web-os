from instruction_loader import Instruction_loader

instruction_loader = Instruction_loader()

with open('programs/factorial.ch') as f:
    lines = [line.rstrip() for line in f]

for instruction in lines:
    instruction_loader.parse_and_compile(instruction)

instruction_loader.run_all()
