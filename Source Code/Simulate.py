from Classes import ReservationStation, CommonDataBus, InstructionQueue, RegisterFile, Memory, FunctionalUnit
import io
import sys
class Simulation():
    def __init__(self, InstructionQueue):
        self.cycles = 0
        self.reservation_stations = [
            ReservationStation('LD'+str(i+1), 'LD', 6) for i in range(2)] + \
            [ReservationStation('SD', 'SD', 6)] + \
            [ReservationStation('BEQ', 'BEQ', 1)] + \
            [ReservationStation('CALL', 'CALL', 1)] + \
            [ReservationStation('RET', 'RET', 1)] + \
            [ReservationStation('ADD'+str(i+1), 'ADD', 2) for i in range(4)] + \
            [ReservationStation('NAND'+str(i+1), 'NAND', 1) for i in range(2)] + \
            [ReservationStation('MUL', 'MUL', 8)
        ]
        self.common_data_bus = CommonDataBus()
        self.instruction_queue = InstructionQueue
        self.register_file = RegisterFile(8)
        self.memory = Memory(128)
    def set_memory(self, address, value):
        self.memory.store(address, value)
    def set_instruction_queue(self, instructions):
        self.instruction_queue = instructions

    


    def simulate(self, flag):
        if not flag:
            self.cycles = 0
        if True:
            string = ""
            self.common_data_bus.busy = False
            
            # Execute Function 
            # the order of execute and fetch is flipped because i don't want to fetch then execute in the same cycle. 
            for reservation_station in self.reservation_stations:
                if reservation_station.busy and reservation_station.op.execution_time != 0:
                    if reservation_station.vj is not None and reservation_station.vk is not None:
                        reservation_station.op.operand1 = reservation_station.vj
                        reservation_station.op.operand2 = reservation_station.vk
                        reservation_station.op.execute()  # Execute the operation
                        reservation_station.op.execution_time -= 1
                        string += f"Executing {reservation_station.op.operation} in {reservation_station.name}\n"
                        string += f"Execution time remaining: {reservation_station.op.execution_time}\n"
                        if reservation_station.op.operation == 'LD': 
                            if reservation_station.op.execution_time == 4:
                                reservation_station.a = reservation_station.op.result
                        if reservation_station.op.operation == 'SD': 
                            if reservation_station.op.execution_time == 4:
                                reservation_station.a = reservation_station.op.result
                elif reservation_station.busy and not self.common_data_bus.busy:
                    # Writeback Function
                    self.common_data_bus.busy = True
                    string += f"Writing back {reservation_station.op.operation} in {reservation_station.name}\n"
                    string += f"Result: {reservation_station.op.result}\n"
                    
                    if reservation_station.op.operation == 'LD':
                        self.common_data_bus.value = self.memory.load(reservation_station.a)
                        self.register_file.status[reservation_station.dest].Qi = None
                        if reservation_station.dest != 0:  
                            self.register_file.registers[reservation_station.dest].value = self.common_data_bus.value  # Update register file value
                        reservation_station.busy = False
                        for rs in self.reservation_stations:
                            if rs.qj == reservation_station.name:
                                rs.vj = self.common_data_bus.value
                                rs.qj = None
                            if rs.qk == reservation_station.name:
                                rs.vk = self.common_data_bus.value
                                rs.qk = None
                    elif reservation_station.op.operation == 'SD':
                        self.common_data_bus.value = self.register_file.registers[reservation_station.dest].value
                        self.register_file.status[reservation_station.dest].Qi = None
                        self.memory.store(reservation_station.a,self.common_data_bus.value)   # Update register file value
                        reservation_station.busy = False
                        for rs in self.reservation_stations:
                            if rs.qj == reservation_station.name:
                                rs.vj = self.common_data_bus.value
                                rs.qj = None
                            if rs.qk == reservation_station.name:
                                rs.vk = self.common_data_bus.value
                                rs.qk = None
                    elif reservation_station.op.operation == 'BEQ':
                        self.common_data_bus.value = reservation_station.op.result
                        self.instruction_queue.jump(reservation_station.vk + 1 + reservation_station.qk)
                        print(reservation_station.vk + 1 + reservation_station.qk)
                        reservation_station.busy = False
                        for rs in self.reservation_stations:
                            if rs.qj == reservation_station.name:
                                rs.vj = self.common_data_bus.value
                                rs.qj = None
                            if rs.qk == reservation_station.name:
                                rs.vk = self.common_data_bus.value
                                rs.qk = None
                    elif reservation_station.op.operation == 'RET':
                        self.common_data_bus.value = self.register_file.registers[1].value
                        self.register_file.status[reservation_station.dest].Qi = None
                        self.instruction_queue.jump(self.common_data_bus.value)
                        reservation_station.busy = False
                        for rs in self.reservation_stations:
                            if rs.qj == reservation_station.name:
                                rs.vj = self.common_data_bus.value
                                rs.qj = None
                            if rs.qk == reservation_station.name:
                                rs.vk = self.common_data_bus.value
                                rs.qk = None
                    elif reservation_station.op.operation == 'CALL':
                        self.common_data_bus.value = reservation_station.qj + 1 # Ali: ALLLLIIIIIIIIIIIIIIIII
                        self.register_file.registers[1] = self.common_data_bus.value
                        self.register_file.status[reservation_station.dest].Qi = None
                        self.instruction_queue.jump(self.register_file.registers[reservation_station.vj].value)
                        reservation_station.busy = False
                        for rs in self.reservation_stations:
                            if rs.qj == reservation_station.name:
                                rs.vj = self.common_data_bus.value
                                rs.qj = None
                            if rs.qk == reservation_station.name:
                                rs.vk = self.common_data_bus.value
                                rs.qk = None
                    else: 
                        self.common_data_bus.value = reservation_station.op.result
                        self.register_file.status[reservation_station.dest].Qi = None
                        if reservation_station.dest != 0:  # Replace non-standard character with a colon
                            self.register_file.registers[reservation_station.dest].value = self.common_data_bus.value  # Update register file value
                        reservation_station.busy = False
                        for rs in self.reservation_stations:
                            if rs.qj == reservation_station.name:
                                rs.vj = self.common_data_bus.value
                                rs.qj = None
                            if rs.qk == reservation_station.name:
                                rs.vk = self.common_data_bus.value
                                rs.qk = None

            flagbr = False
            # ISSUE Function
            for instruction in self.instruction_queue.instructions:
                for reservation_station in self.reservation_stations:

                    if reservation_station.op.operation == instruction.op or (reservation_station.op.operation == 'ADD' and instruction.op == 'ADDI'):
                        if not reservation_station.busy:
                            self.instruction_queue.dequeue(instruction)
                            reservation_station.busy = True
                            reservation_station.op = FunctionalUnit(instruction.op, reservation_station.op.execution_time)
                            src1_index = int(instruction.src1[1:])  # Convert register name to index
                            dest_index = int(instruction.dest[1:])  # Convert register name to index
                            reservation_station.dest = dest_index
                            if self.register_file.status[src1_index].Qi is None:
                                reservation_station.vj = self.register_file.registers[src1_index].value
                            else:
                                reservation_station.qj = self.register_file.status[src1_index].Qi
                            if instruction.op == 'BEQ':
                                reservation_station.vk = int(instruction.src2)  # Treat src2 as an immediate value
                                reservation_station.qk = self.instruction_queue.current_index
                            if instruction.op == 'CALL':
                                reservation_station.vj = 1
                                reservation_station.qj = self.instruction_queue.current_index
                                reservation_station.vk = int(instruction.src1)
                            if instruction.op == 'RET':
                                reservation_station.vj = 1
                                reservation_station.qj = self.instruction_queue.current_index
                            elif instruction.src2 is not None:
                                if instruction.src2.isnumeric():
                                    reservation_station.vk = int(instruction.src2)
                                else:
                                    src2_index = int(instruction.src2[1:])  # Convert register name to index
                                    if self.register_file.status[src2_index].Qi is None:
                                        reservation_station.vk = self.register_file.registers[src2_index].value
                                    else:
                                        reservation_station.qk = self.register_file.status[src2_index].Qi
                            dest_index = int(instruction.dest[1:])  # Convert register name to index
                            self.register_file.status[dest_index].Qi = reservation_station.name
                            flagbr = True
                            break
                if flagbr: break 
                

            output = io.StringIO()
            sys.stdout = output
            
            # Print Functions
            print(f"Cycle {self.cycles}:")
            self.instruction_queue.print_instructions()
            
            self.register_file.print_registers()

            self.register_file.print_registers_status()
            for reservation_station in self.reservation_stations:
                reservation_station.print_reservation_station()
            sys.stdout = sys.__stdout__
            string += output.getvalue()
            
            
            self.cycles += 1
            return string


        