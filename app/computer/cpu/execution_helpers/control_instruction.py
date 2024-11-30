from computer.cycle_state import CycleState
from computer.assembly.opcodes_and_types import OpcodesAndTypes
from computer.computer_state import ComputerState


def execute_control_instruction(computer_state: ComputerState):
    codop = computer_state.system_registers.ir[0:4]
    etiqueta = computer_state.system_registers.ir[6:10]
    if codop == OpcodesAndTypes.opcodes.get("JMP"):
        computer_state.system_registers.pc = etiqueta
    elif codop == OpcodesAndTypes.opcodes.get("JZ"):
        if computer_state.psw.zero:
            computer_state.system_registers.pc = etiqueta
        else:
            computer_state.system_registers.pc = (
                f"{int(computer_state.system_registers.pc, 2) + 1:04b}"
            )
    elif codop == OpcodesAndTypes.opcodes.get("JN"):
        if computer_state.psw.negative:
            computer_state.system_registers.pc = etiqueta
        else:
            computer_state.system_registers.pc = (
                f"{int(computer_state.system_registers.pc, 2) + 1:04b}"
            )
    else:
        raise ValueError(f"Operación no soportada: {codop}")
    computer_state.cycle = CycleState.FETCH_INS
