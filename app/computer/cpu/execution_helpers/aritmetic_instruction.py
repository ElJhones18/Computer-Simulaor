from computer.cycle_state import CycleState
from computer.assembly.opcodes_and_types import OpcodesAndTypes
from computer.computer_state import ComputerState

fetch_signal: str = "1"
write_signal: str = "0"


def fetch_operands(computer_state: ComputerState):
    """Ejecuta una instrucción aritmética"""
    operand1 = computer_state.system_registers.ir[4:10]
    operand2 = computer_state.system_registers.ir[10:16]

    if computer_state.actual_micro_operation < 7:
        fetch_operand1(operand1, computer_state)
    elif computer_state.actual_micro_operation >= 7:
        fetch_operand2(operand2, computer_state)


def execute_operation(computer_state: ComputerState):
    match computer_state.actual_micro_operation:
        case 0:
            try:
                computer_state.alu.execute_operation()
                computer_state.actual_micro_operation += 1
            except ValueError as e:
                computer_state.cycle = CycleState.WAITING
                computer_state.actual_micro_operation = 0
        case 1:
            if len(computer_state.alu.result) > 16:
                computer_state.psw.overflow = True
                computer_state.cycle = CycleState.WAITING
            if int(computer_state.alu.result) == 0:
                computer_state.psw.zero = True
            if int(computer_state.alu.result) < 0:
                computer_state.psw.negative = True
            computer_state.cycle = CycleState.WRITE
            computer_state.actual_micro_operation = 0


def fetch_operand2(operand: str, computer_state: ComputerState):
    type = operand[:2]
    value = operand[2:6]
    if type == OpcodesAndTypes.TIPO_NUMERO:
        computer_state.alu.operator2 = value
        computer_state.actual_micro_operation = 0
        computer_state.cycle = CycleState.EXECUTE
    elif type == OpcodesAndTypes.TIPO_REGISTRO:
        op = computer_state.user_registers.get_register("R" + f"{int(value, 2)}")
        computer_state.alu.operator2 = op
        computer_state.actual_micro_operation = 0
        computer_state.cycle = CycleState.EXECUTE
    elif type == OpcodesAndTypes.TIPO_MEMORIA:
        read_memory_value2(value, computer_state)
    else:
        raise ValueError(f"Tipo de operando inválido: {type}")


def fetch_operand1(operand: str, computer_state: ComputerState):
    type = operand[:2]
    value = operand[2:6]
    if type == OpcodesAndTypes.TIPO_REGISTRO:
        op = computer_state.user_registers.get_register("R" + f"{int(value, 2)}")
        computer_state.alu.operator1 = op
        codop = computer_state.system_registers.ir[0:4]
        if codop == OpcodesAndTypes.opcodes.get("ADD"):
            computer_state.alu.operation = "+"
        elif codop == OpcodesAndTypes.opcodes.get("SUB"):
            computer_state.alu.operation = "-"
        elif codop == OpcodesAndTypes.opcodes.get("MUL"):
            computer_state.alu.operation = "*"
        elif codop == OpcodesAndTypes.opcodes.get("DIV"):
            computer_state.alu.operation = "/"
        computer_state.actual_micro_operation = 7
    elif type == OpcodesAndTypes.TIPO_MEMORIA:
        read_memory_value1(value, computer_state)
    else:
        raise ValueError(f"Tipo de operando inválido: {type}")


def read_memory_value1(address: str, computer_state: ComputerState):
    match computer_state.actual_micro_operation:
        case 0:
            computer_state.system_bus.control_bus = fetch_signal
            computer_state.actual_micro_operation += 1
        case 1:
            computer_state.system_registers.mar = address
            computer_state.actual_micro_operation += 1
        case 2:
            computer_state.system_bus.address_bus = computer_state.system_registers.mar
            computer_state.actual_micro_operation += 1
        case 3:
            computer_state.system_bus.data_bus = computer_state.data_memory.read(
                address
            )
            computer_state.actual_micro_operation += 1
        case 4:
            computer_state.system_registers.mbr = computer_state.system_bus.data_bus
            computer_state.actual_micro_operation += 1
        case 5:
            computer_state.alu.operator1 = computer_state.system_registers.mbr
            computer_state.actual_micro_operation += 1
        case 6:
            codop = computer_state.system_registers.ir[0:4]
            if codop == OpcodesAndTypes.opcodes.get("ADD"):
                computer_state.alu.operation = "+"
            elif codop == OpcodesAndTypes.opcodes.get("SUB"):
                computer_state.alu.operation = "-"
            elif codop == OpcodesAndTypes.opcodes.get("MUL"):
                computer_state.alu.operation = "*"
            elif codop == OpcodesAndTypes.opcodes.get("DIV"):
                computer_state.alu.operation = "/"
            computer_state.actual_micro_operation += 1


def read_memory_value2(address: str, computer_state: ComputerState):
    match computer_state.actual_micro_operation:
        case 7:
            computer_state.system_bus.control_bus = fetch_signal
            computer_state.actual_micro_operation += 1
        case 8:
            computer_state.system_registers.mar = address
            computer_state.actual_micro_operation += 1
        case 9:
            computer_state.system_bus.address_bus = computer_state.system_registers.mar
            computer_state.actual_micro_operation += 1
        case 10:
            computer_state.system_bus.data_bus = computer_state.data_memory.read(
                address
            )
            computer_state.actual_micro_operation += 1
        case 11:
            computer_state.system_registers.mbr = computer_state.system_bus.data_bus
            computer_state.actual_micro_operation += 1
        case 12:
            computer_state.alu.operator2 = computer_state.system_registers.mbr
            computer_state.actual_micro_operation = 0
            computer_state.cycle = CycleState.EXECUTE
