from .algorithm import Algorithm
from tabulate   import tabulate
from copy       import copy
import traceback

class RoundRobin(Algorithm):
    #Shortest job first
    def __init__(self, run_instances, quantum):
        super().__init__()
        self.run_instances     = run_instances
        self.quantum           = quantum
        self.order             = None
        self.ordered_instances = None
        self.num_lines_to_run_all_instances = None
        self.possible_queue    = None
        self.currentLineRunInstance = None
        self.currentNumberLinesToRun = None
        self.linesRan               = 0

    def getRunInstances(self):
        return self.run_instances

    def getOrder(self):
        instances = self.order
        names    = []
        for item in instances:
            names.append(item.getFilename())

        concat = []
        id_ = 1
        for name in names:
            concat.append((id_, name))
            id_ += 1
        return concat

    def orderRunInstancesRound(self):
        self.orderRunInstancesByArrival()
        self.ordered_instances = self.run_instances.copy()
        ######################################
        self.memory = self.getMemory(self.run_instances)
        originalInstructionDictionary = self.memory.getDeclarationInstructionDictionary()
        instructionDictionary = {}
        for key in originalInstructionDictionary:
            instructionDictionary[key] = originalInstructionDictionary[key].copy()
        timeToRunAll = self.time.getTimeToRunAllInstances()
        new_order_run_instances         = []
        num_lines_to_run_all_instances = []
        current_time     = 0
        lines_to_run = 0
        quantum_timer = 0
        declarationHistory = self.memory.declarationHistory

        print(f"numInstructionsAllinstances: {timeToRunAll}")
        while(current_time < timeToRunAll):
            possible = self.runnableInstances(current_time) 
            self.printPossible(possible) 
            instance = possible[0]
            self.time.substractFromCPU(instance,  1)

            declaration = instance.progDefs.getDeclaration()
            instructions = instructionDictionary[declaration]
            print(f"instructions: {instructions}")
            if len(instructions) == 1:
                lines_to_run +=1
                instructionDictionary[declaration] = []
            else:
                if len(instructions) != 0:
                    instructions.pop(0)
                    instructionDictionary[declaration] = instructions
                    lines_to_run +=1
            print(f"chosen instance: {instance.getFilename()}, current cpu burst: {self.time.getCurrentCpuBurst(instance)}, lines to run: {lines_to_run}, quantum: {self.time.getQuantum()}")


            quantum_timer += 1
            #if instance is finished then add it to the list
            if self.time.getCurrentCpuBurst(instance) == 0:
                # print("did it 1")
                num_lines_to_run_all_instances.append(lines_to_run)
                new_order_run_instances.append(instance)
                self.removeInstanceFromQueue()
                current_time +=1
                lines_to_run = 0
                quantum_timer = 0
                print(f"checked: {self.instancesToReadable(new_order_run_instances)}\n_______________________\n")
                continue
            else:
                #if quantum limit reached, append 
                if quantum_timer == self.time.getQuantum():
                    num_lines_to_run_all_instances.append(lines_to_run)
                    new_order_run_instances.append(instance)
                    self.putInstanceInTheBack()
                    current_time +=1
                    lines_to_run = 0
                    quantum_timer = 0
                    print(f"checked: {self.instancesToReadable(new_order_run_instances)}\n_______________________\n")
                    continue

            print(f"checked: {self.instancesToReadable(new_order_run_instances)}\n_______________________\n")
            current_time += 1
        self.run_instances = new_order_run_instances
        self.num_lines_to_run_all_instances = num_lines_to_run_all_instances

    def removeInstanceFromQueue(self):
        self.possible_queue.pop(0)


    def putInstanceInTheBack(self):
        for pos in self.possible_queue:
            print("previous possible", pos[0].getFilename())
        current_instance = self.possible_queue.pop(0)
        self.possible_queue.append(current_instance)
        for pos in self.possible_queue:
            print("new possible", pos[0].getFilename())

    def instancesToReadable(self, run_instances):
        names = []
        for instance in run_instances:
            names.append(instance.getFilename())
        return names

    def getNumInstructionsInAllInstances(self):
        self.memory = self.getMemory(self.run_instances)
        instructions_all_instances = self.memory.get_programs()
        totalNumInstructions = 0
        for instructions in instructions_all_instances:
            totalNumInstructions += len(instructions)
        return totalNumInstructions

    def orderRunInstancesByArrival(self):
        self.time.setArrivalTimes(self.run_instances)
        self.time.setCpuBursts(self.run_instances)
        arrive_times = list(self.time.arrive_times.items())
        arrive_times.sort(key= lambda tuple: tuple[1])
        
        self.run_instances.clear()
        for elem in arrive_times:
            self.run_instances.append(elem[0])
    
    def runnableInstances(self, current_time):
        if self.possible_queue == None:
            self.possible_queue = self.time.getSortedArrivalTimes()
        arrive_times = self.possible_queue
        possible = []
        for time in arrive_times:
            if time[1] <= current_time and self.time.getCurrentCpuBurst(time[0]) > 0:
                possible.append(time[0])
        return possible

    def findShortestJob(self, instances_possible):
        shortest = 99999999
        answer  = None
        for instance in instances_possible:
            if self.time.getCurrentCpuBurst(instance) < shortest:
                answer = instance
                shortest = self.time.getCurrentCpuBurst(instance)
        return answer

    def extractFromTimeAndCpu(self, instance): #TODO make it work without time object, but a queue object wrapper that uses cpu, time, and runners
        times    = self.time.getArrivalTimes()
        cpu      = self.time.getCpuBursts()
        times    = times.pop(instance, None)
        cpu      = cpu.pop(instance, None)
        return times, cpu


    def printPossible(self, possible):
        for each in possible:
            print("possible: ", each.getFilename())
        print("\n")
        for instance2,cpu in self.time.getCpuBursts().items():
            print(f"{instance2.getFilename()},  arrival: {self.time.getArrivalTime(instance2)},  cpu: {cpu}")

    def setup(self):
        self.time.setQuantum(self.quantum)
        self.orderRunInstancesRound()
        

    def run(self):
        num_instances = len(self.run_instances)
        self.order = self.run_instances.copy()
        instance = None
        print(f"to run: ")
        names = self.instancesToReadable(self.run_instances)
        for name, lines in zip(names,self.num_lines_to_run_all_instances):
            print(name," ", lines)
        for i in range(num_instances):              #! error esta aqui
            instance = self.run_instances.pop(0)
            print(f"going to run: {instance.getFilename()}, this many lines: {self.num_lines_to_run_all_instances[0]}")
            instance.run_all_expro(self.num_lines_to_run_all_instances.pop(0))
        
        
    def runLine(self):
        if self.currentLineRunInstance == None and len(self.run_instances) == 0:
            print("nothing more to run")
            return 
        else:
            if self.currentLineRunInstance == None:
                self.currentLineRunInstance = self.run_instances.pop(0)
                self.currentNumberLinesToRun = self.num_lines_to_run_all_instances.pop(0)
                while self.currentNumberLinesToRun == 0 and len(self.num_lines_to_run_all_instances) != 0:
                    self.currentLineRunInstance = self.run_instances.pop(0)
                    self.currentNumberLinesToRun = self.num_lines_to_run_all_instances.pop(0)
                if len(self.num_lines_to_run_all_instances) == 0 and self.currentNumberLinesToRun == 0:
                    queues = self.memory.getQueues()
                    queues.clearPendingRunInstances()
                    print(f"pending programs: {queues.getPendingRunInstances()}")
                    print("nothing more to run. 2")
                    self.currentLineRunInstance = None
                    self.currentNumberLinesToRun = None
                    return
        print(f"currentlineRunInstance: {self.currentLineRunInstance}, num run instances: {len(self.run_instances)}")
        itRan = self.currentLineRunInstance.run_line()
        declaration = self.currentLineRunInstance.progDefs.getDeclaration() 
        dataStream = self.memory.getDataStream()
        dataStream.clearSteps() 
        if itRan:
            stepsInRunner = self.currentLineRunInstance.get_operators_executed_history() 
            step = stepsInRunner.pop(0)
            line = step[0]
            instructionName = step[1]
            instructionName = " ".join(step[1])
            message = "line: " + str(line) + " " + str(instructionName) + " | " + self.memory.getSteps(declaration).pop() #!
            print(f"entered here, where it ran, the message is: {message}")
            dataStream.appendStep(declaration, message)
        else:
            queues = self.memory.getQueues()
            compiler = queues.getCompilerFromDeclaration(declaration)
            stepsInCompiler = compiler.get_declarations_executed_history()
            if len(stepsInCompiler) > 0:
                step = stepsInCompiler.pop(0)
                line = step[0]
                instructionName = step[1]
                instructionName = " ".join(step[1])
                message = "line: " + str(line) + " " + str(instructionName) + " | " + self.memory.getSteps(declaration).pop(0) #!
                print(f"entered here, where it did not run, the message is: {message}")
                dataStream.appendStep(declaration, message)

        current_line = self.currentLineRunInstance.getCurrentLine()
        length_program = len(self.memory.getInstructionFromDeclaration(declaration))
        self.linesRan += 1
        finished = True if  self.linesRan == self.currentNumberLinesToRun or current_line == length_program else False
        if finished: 
            print("it finished..................................")
            self.currentLineRunInstance = None
            self.currentNumberLinesToRun = None
            self.linesRan = 0


    def getTable(self):
        instances = self.ordered_instances
        arrival   = []
        for instance in instances:
            arrival.append(self.time.getArrivalTime(instance))

        cpu  = []
        for instance in instances:
            cpu.append(self.time.getCpuBurst(instance))

        table = []
        for instance,arr, cp in zip(instances,arrival,cpu):
            table.append([instance.getFilename(), arr, cp])
        return tabulate(table, headers=['Nombre', 'Tiempo de llegada', 'Rafaga de cpu'], tablefmt='orgtbl')
