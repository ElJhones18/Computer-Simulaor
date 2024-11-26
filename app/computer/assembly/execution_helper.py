from computer.cycle_state import CycleState
from computer.computer_state import ComputerState
from computer.assembly.opcodes_and_types import OpcodesAndTypes

fetch_signal: str = "1"
write_signal: str = "0"


def execute_transfer_instruction(computer_state: ComputerState):
    """Ejecuta una instrucción de transferencia"""
    opcode = computer_state.system_registers.ir[:4]
    if opcode == OpcodesAndTypes.opcodes.get("MOV"):
        operand1 = computer_state.system_registers.ir[4:10]
        operand2 = computer_state.system_registers.ir[10:16]
        if computer_state.fetching_operand:
            origin: str = get_origin(operand2, computer_state)
        if not computer_state.fetching_operand:
            if operand1[:2] == OpcodesAndTypes.TIPO_REGISTRO:
                computer_state.user_registers.set_register(
                    f"R{int(operand1[2:6], 2)}", origin
                )
                computer_state.cycle = CycleState.FETCH_INS
                computer_state.system_registers.pc = (
                    f"{int(computer_state.system_registers.pc, 2) + 1:04b}"
                )
                computer_state.fetching_operand = True
            elif operand1[:2] == OpcodesAndTypes.TIPO_MEMORIA:
                fetch_memory_value(computer_state, operand1[2:6], write=True)
            else:
                raise ValueError(f"Operación no soportada: {opcode}")
    else:
        raise ValueError(f"Operación no soportada: {opcode}")


def get_origin(operand: str, computer_state: ComputerState):
    type = operand[:2]
    value = operand[2:6]
    if type == OpcodesAndTypes.TIPO_NUMERO:
        if computer_state.system_registers.ir[4:6] == OpcodesAndTypes.TIPO_MEMORIA:
            computer_state.system_registers.mbr = value
        computer_state.fetching_operand = False
        return value
    elif type == OpcodesAndTypes.TIPO_REGISTRO:
        if computer_state.system_registers.ir[4:6] == OpcodesAndTypes.TIPO_MEMORIA:
            computer_state.system_registers.mbr = (
                computer_state.user_registers.get_register("R" + f"{int(value, 2)}")
            )
        computer_state.fetching_operand = False
        return computer_state.user_registers.get_register("R" + f"{int(value, 2)}")
    elif type == OpcodesAndTypes.TIPO_MEMORIA:
        return fetch_memory_value(computer_state, value)
    else:
        raise ValueError(f"Tipo de operando inválido: {type}")


def fetch_memory_value(computer_state: ComputerState, addr, write=False):
    match computer_state.actual_micro_operation:
        case 0:
            if write:
                computer_state.system_bus.control_bus = write_signal
            else:
                computer_state.system_bus.control_bus = fetch_signal
            computer_state.actual_micro_operation += 1
        case 1:
            computer_state.system_registers.mar = addr
            computer_state.actual_micro_operation += 1
        case 2:
            computer_state.system_bus.address_bus = computer_state.system_registers.mar
            computer_state.actual_micro_operation += 1
        case 3:
            if not write:
                computer_state.system_bus.data_bus = computer_state.data_memory.read(
                    computer_state.system_registers.mar
                )
            else:
                computer_state.system_bus.data_bus = computer_state.system_registers.mbr
            computer_state.actual_micro_operation += 1
        case 4:
            if not write:
                computer_state.system_registers.mbr = computer_state.system_bus.data_bus
                computer_state.fetching_operand = False
            else:
                computer_state.data_memory.write(
                    addr, computer_state.system_registers.mbr
                )
                computer_state.cycle = CycleState.FETCH_INS
                computer_state.system_registers.pc = (
                    f"{int(computer_state.system_registers.pc, 2) + 1:04b}"
                )
                computer_state.fetching_operand = True
            computer_state.actual_micro_operation = 0
            return computer_state.system_registers.mbr
