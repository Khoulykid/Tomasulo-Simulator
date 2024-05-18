class ReservationStation:
    def __init__(self, name=None, op=None, execution_time=None):
        self.name = name
        self.busy = False
        self.op = FunctionalUnit(op, execution_time)
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.dest = None # this shouldn't be displayed in the print_reservation_station but i use it to write back 
        self.a = None


    def print_reservation_station(self):
        print(f"{self.name}: {self.busy}, {self.op.operation}, {self.vj}, {self.vk}, {self.qj}, {self.qk}, {self.dest}, {self.a}, {self.op.execution_time}") # Ali: remove dest and remaining time at the end  

class FunctionalUnit: 
    def __init__(self, operation, execution_time):
        self.operation = operation 
        self.execution_time = execution_time
        self.operand1 = None
        self.operand2 = None
        self.result = None

    def execute(self):
        if self.operation == 'MUL':
            self.result = self.operand1 * self.operand2
        elif self.operation == 'NAND':
            self.result = ~(self.operand1 & self.operand2)
        elif self.operation == 'ADD' or self.operation == 'ADDI':
            self.result = self.operand1 + self.operand2
        # Ali: add other operations here. 
        # Take care that Load/Store have address computations that should be written in reservation stations. 
        # make sure to solve the issue where there's two things writing to the same address 
        # slide 10 and 11 lecture 17 this semester 
        #actually the result is ready from the first moment but we write it back after the execution time is finished. 


class CommonDataBus: #Ali: debug to see if two operations write at the same time 
    def __init__(self):
        self.busy = False
        self.value = None

class Instruction:
    def __init__(self, op, dest, src1, src2=None):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2

    def print_instruction(self):
        print(f"{self.op}, {self.dest}, {self.src1}, {self.src2}")

class InstructionQueue: 
    def __init__(self):
        self.instructions = [
            Instruction('ADD', 'R5', 'R0', 'R1'),
            Instruction('ADD', 'R2', 'R5', 'R4') 
        ]

    def enqueue(self, instruction):
        self.instructions.append(instruction)

    def dequeue(self): # I'm not sure this this dequeue removes the first instruction or the instruction just fetched 
        #imagine a scenario where the reservation station is not empty, then i want to fetch the next instruction and dequeue the other instruction 
        # check if the dequeue happens on the correct instruction not the first one
        # i don't know the behavior of the lists in python 

        return self.instructions.pop(0) if self.instructions else None

    def print_instructions(self):
        for instruction in self.instructions:
            instruction.print_instruction()

class Register:
    def __init__(self):
        self.value = None

class RegisterFile:
    def __init__(self, size):
        self.registers = [Register() for _ in range(size)]
        self.status = [RegisterStatus() for _ in range(size)]  # I creat a regfile, for each reg there's a status. This is the two rows in the bottom of the slides
        self.initialize_registers()
    
    def initialize_registers(self):
        for i, register in enumerate(self.registers):
            register.value = i # you know the typical R0 = 0, R1 = 1 
        # Ali: Hardwire the 0 to 0 
        
    def print_registers(self):
        for i, register in enumerate(self.registers):
            print(f"R{i}: {register.value}")

    def print_registers_status(self):
        for i, register in enumerate(self.status):
            print(f"R{i} status : {register.Qi}")

class RegisterStatus:
    def __init__(self):
        self.Qi = None

    def print_status(self):
        print(f"Qi: {self.Qi}")


class Memory: # Ali: do the initialization of the memory and check the size of the memory 
                # it should be 128kb and word addressable where each word is 16-bit 
    def __init__(self, size):
        self.data = [0] * size

    def load(self, address):
        return self.data[address]

    def store(self, address, value):
        self.data[address] = value

def simulate():
    reservation_stations = [
        ReservationStation('LOAD'+str(i+1), 'LOAD', 6) for i in range(2)] + \
        [ReservationStation('STORE', 'STORE', 6)] + \
        [ReservationStation('BEQ', 'BEQ', 1)] + \
        [ReservationStation('CALL/RET', 'CALL/RET', 1)] + \
        [ReservationStation('ADD'+str(i+1), 'ADD', 2) for i in range(4)] + \
        [ReservationStation('NAND'+str(i+1), 'NAND', 1) for i in range(2)] + \
        [ReservationStation('MUL', 'MUL', 8)
    ]


    common_data_bus = CommonDataBus()
    instruction_queue = InstructionQueue()
    register_file = RegisterFile(8)
    memory = Memory(1024) # Ali: i totally disregarded the memory here 

    cycles = 0
    while True:
        print(f"Cycle:  {cycles}")
        common_data_bus.busy = False
         
        # Execute Function 
        # the order of execute and fetch is flipped because i don't want to fetch then execute in the same cycle. 
        for reservation_station in reservation_stations:
            if reservation_station.busy and reservation_station.op.execution_time != 0:
                if reservation_station.vj is not None and reservation_station.vk is not None:
                    reservation_station.op.operand1 = reservation_station.vj
                    reservation_station.op.operand2 = reservation_station.vk
                    reservation_station.op.execute()  # Execute the operation
                    reservation_station.op.execution_time -= 1
                    print(f"Executing {reservation_station.op.operation} in {reservation_station.name}")
                    print(f"Execution time remaining: {reservation_station.op.execution_time}")
            elif reservation_station.busy and not common_data_bus.busy:
                # Writeback Function
                common_data_bus.busy = True
                print(f"Writing back {reservation_station.op.operation} in {reservation_station.name}")
                print(f"Result: {reservation_station.op.result}")
                common_data_bus.value = reservation_station.op.result
                register_file.status[reservation_station.dest].Qi = None
                register_file.registers[reservation_station.dest].value = common_data_bus.value  # Update register file value
                reservation_station.busy = False
                for rs in reservation_stations:
                    if rs.qj == reservation_station.name:
                        rs.vj = common_data_bus.value
                        rs.qj = None
                    if rs.qk == reservation_station.name:
                        rs.vk = common_data_bus.value
                        rs.qk = None

        # FETCH Function
        for instruction in instruction_queue.instructions:
            for reservation_station in reservation_stations:
                if reservation_station.op.operation == instruction.op:
                    if not reservation_station.busy:
                        instruction_queue.dequeue()
                        reservation_station.busy = True
                        reservation_station.op = FunctionalUnit(instruction.op, reservation_station.op.execution_time)
                        src1_index = int(instruction.src1[1:])  # Convert register name to index
                                                                # This should be implemented above not here but ok for now 
                        dest_index = int(instruction.dest[1:])  # Convert register name to index
                                                                # This should be implemented above not here but ok for now 
                        reservation_station.dest = dest_index
                        if register_file.status[src1_index].Qi is None:
                            reservation_station.vj = register_file.registers[src1_index].value
                        else:
                            reservation_station.qj = register_file.status[src1_index].Qi
                        if instruction.src2 is not None:
                            src2_index = int(instruction.src2[1:])  # Convert register name to index
                            if register_file.status[src2_index].Qi is None:
                                reservation_station.vk = register_file.registers[src2_index].value
                            else:
                                reservation_station.qk = register_file.status[src2_index].Qi
                        dest_index = int(instruction.dest[1:])  # Convert register name to index
                        register_file.status[dest_index].Qi = reservation_station.name
                        break

       
        # Print Functions
        instruction_queue.print_instructions()
        register_file.print_registers()
        register_file.print_registers_status()
        for reservation_station in reservation_stations:
            reservation_station.print_reservation_station()

        
        # Ali: I run for 7 cycles. you run untill all the instructions are done.
        if cycles == 7:
            break
        
        cycles += 1


    return cycles

simulate()