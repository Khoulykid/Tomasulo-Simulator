from Classes import ReservationStation, CommonDataBus, InstructionQueue, RegisterFile, Memory, FunctionalUnit
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
    memory = Memory(128) # Ali: i totally disregarded the memory here 

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