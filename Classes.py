import numpy as np
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
        print(f"{self.name}: {self.busy}, {self.op.operation}, {self.vj}, {self.vk}, {self.qj}, {self.qk}, {self.a}, {self.op.execution_time}") # 

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
        elif self.operation == 'BEQ':
            if self.operand1 == self.operand2:
                self.result = 1
            else:
                self.result = 0
        elif self.operation == 'LD':
            self.result = self.operand1 + self.operand2
        elif self.operation == 'SD':
            self.result = self.operand1 + self.operand2
        elif self.operation == 'RET': 
            self.result = self.operand1
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
        self.og = []
        self.instructions = []
        self.current_index = 0

    def enqueue(self, instruction):
        self.instructions.append(instruction)
        self.og.append(instruction)

    def jump(self, target_index):
        if 0 <= target_index < len(self.og):
            self.instructions = self.og[target_index:]
            self.current_index = target_index

        else:
            self.instructions = []

    def dequeue(self, instruction):
        self.instructions.remove(instruction)
        self.current_index += 1

    def empty(self):
        return len(self.instructions) == 0

    def print_instructions(self):
        for instruction in self.instructions:
            instruction.print_instruction()

class Register:
    def __init__(self):
        self.value = np.int16(0)

class RegisterFile:
    def __init__(self, size):
        self.registers = [Register() for _ in range(size)]
        self.status = [RegisterStatus() for _ in range(size)]  # I creat a regfile, for each reg there's a status. This is the two rows in the bottom of the slides
        self.initialize_registers()
    
    def initialize_registers(self):
        for i, register in enumerate(self.registers):
            register.value = np.int16(i) # you know the typical R0 = 0, R1 = 1 
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
        self.data = np.zeros(size*1000//16, dtype=np.int16)

    def load(self, address):
        if 0 <= address < len(self.data):
            return self.data[address]
        else:
            raise IndexError("Address out of range")

    def store(self, address, value):
        if 0 <= address < len(self.data):
            self.data[address] = value
        else:
            raise IndexError("Address out of range")
