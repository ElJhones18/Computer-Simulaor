from computer.computer_state import ComputerState
from computer.cycle_state import CycleState
import streamlit as st
from computer.assembly.opcodes_and_types import OpcodesAndTypes
from computer.cpu.execution_helpers.transfer_instruction import (
    execute_transfer_instruction,
)
from computer.cpu.execution_helpers.aritmetic_instruction import (
    fetch_operands,
    execute_operation,
)


class ControlUnit:
    def __init__(self):
        self.opcodes = OpcodesAndTypes.opcodes
        self.TIPO_NUMERO = OpcodesAndTypes.TIPO_NUMERO
        self.TIPO_REGISTRO = OpcodesAndTypes.TIPO_REGISTRO
        self.TIPO_MEMORIA = OpcodesAndTypes.TIPO_MEMORIA
        self.TIPO_ETIQUETA = OpcodesAndTypes.TIPO_ETIQUETA

        self.fetch_signal: str = "1"
        self.write_signal: str = "0"

    def instruction_cycle(self, computer_state: ComputerState):
        if computer_state.cycle == CycleState.FETCH_INS:
            self.fetch_instruction(computer_state)
        elif computer_state.cycle == CycleState.DECODE:
            self.decode(computer_state)
        elif (
            computer_state.cycle == CycleState.EXECUTE
            or computer_state.cycle == CycleState.FETCH_OP
        ):
            self.execute_instruction(computer_state)
        elif computer_state.cycle == CycleState.WRITE:
            self.write_output(computer_state)
        return computer_state

    """
    Fetch instruction
    """

    def fetch_instruction(self, computer_state: ComputerState):
        match computer_state.actual_micro_operation:
            case 0:
                computer_state.system_bus.control_bus = self.fetch_signal
                computer_state.actual_micro_operation += 1
            case 1:
                computer_state.system_registers.mar = computer_state.system_registers.pc
                computer_state.actual_micro_operation += 1
            case 2:
                computer_state.system_bus.address_bus = (
                    computer_state.system_registers.mar
                )
                computer_state.actual_micro_operation += 1
            case 3:
                if (
                    computer_state.program_memory.read(
                        computer_state.system_registers.mar
                    )
                    is None
                    or computer_state.program_memory.read(
                        computer_state.system_registers.mar
                    )
                    == "0000000000000000"
                ):
                    computer_state.cycle = CycleState.WAITING
                    computer_state.actual_micro_operation = 0
                else:
                    computer_state.system_bus.data_bus = (
                        computer_state.program_memory.read(
                            computer_state.system_registers.mar
                        )
                    )
                    computer_state.actual_micro_operation += 1
            case 4:
                computer_state.system_registers.mbr = computer_state.system_bus.data_bus
                computer_state.actual_micro_operation += 1
            case 5:
                computer_state.system_registers.ir = computer_state.system_registers.mbr
                computer_state.actual_micro_operation += 1
                computer_state.actual_micro_operation = 0
                computer_state.cycle = CycleState.DECODE

    """
    Decode instruction
    """

    def decode(self, computer_state: ComputerState):
        computer_state.actual_insstruction = self.decode_instruction(
            computer_state.system_registers.ir
        )
        # computer_state.cycle = CycleState.EXECUTE
        computer_state.cycle = CycleState.FETCH_OP

    def decode_operand(self, binary):
        """Decodifica un operando binario a su representación simbólica"""
        tipo = binary[:2]
        valor = int(binary[2:], 2)

        if tipo == self.TIPO_NUMERO:
            return str(valor)
        elif tipo == self.TIPO_REGISTRO:
            return f"R{valor}"
        elif tipo == self.TIPO_MEMORIA:
            return f"#{valor}"
        elif tipo == self.TIPO_ETIQUETA:
            return f"etiq_{valor}"  # Representación simbólica de la etiqueta
        else:
            raise ValueError(f"Tipo de operando inválido: {tipo}")

    def decode_instruction(self, binary):
        """Decodifica una instrucción binaria a su representación simbólica"""
        if len(binary) != 16:
            raise ValueError("La instrucción debe ser de 16 bits")

        # Extraer partes de la instrucción
        opcode_bin = binary[:4]
        operand1_bin = binary[4:10]
        operand2_bin = binary[10:]

        # Encontrar el código de operación
        opcode = None
        for op, code in self.opcodes.items():
            if code == opcode_bin:
                opcode = op
                break

        if opcode is None:
            raise ValueError(f"Código de operación inválido: {opcode_bin}")

        # Decodificar operandos
        operand1 = self.decode_operand(operand1_bin)
        operand2 = self.decode_operand(operand2_bin)

        return f"{opcode} {operand1} {operand2}"

    """
    execute instruction
    """

    def execute_instruction(self, computer_state: ComputerState):
        opcode = computer_state.system_registers.ir[:4]
        if opcode == OpcodesAndTypes.opcodes.get("MOV"):
            execute_transfer_instruction(computer_state)
        elif (
            opcode == OpcodesAndTypes.opcodes.get("ADD")
            or opcode == OpcodesAndTypes.opcodes.get("SUB")
            or opcode == OpcodesAndTypes.opcodes.get("MUL")
            or opcode == OpcodesAndTypes.opcodes.get("DIV")
        ):
            if computer_state.cycle == CycleState.FETCH_OP:
                fetch_operands(computer_state)
            elif computer_state.cycle == CycleState.EXECUTE:
                execute_operation(computer_state)
        elif (
            opcode == OpcodesAndTypes.opcodes.get("JMP")
            or opcode == OpcodesAndTypes.opcodes.get("JZ")
            or opcode == OpcodesAndTypes.opcodes.get("JN")
        ):
            print("Operación de salto")
        else:
            raise ValueError(f"Operación no soportada: {opcode}")

    """write output"""

    def write_output(self, computer_state: ComputerState):
        destination = computer_state.system_registers.ir[4:10]
        type = destination[:2]
        address = destination[2:6]
        if type == self.TIPO_REGISTRO:
            computer_state.user_registers.set_register(
                f"R{int(address, 2)}", computer_state.alu.result
            )
            computer_state.cycle = CycleState.FETCH_INS
            computer_state.system_registers.pc = (
                f"{int(computer_state.system_registers.pc, 2) + 1:04b}"
            )
        elif type == self.TIPO_MEMORIA:
            match computer_state.actual_micro_operation:
                case 0:
                    computer_state.system_bus.control_bus = self.write_signal
                    computer_state.actual_micro_operation += 1
                case 1:
                    computer_state.system_registers.mar = address
                    computer_state.actual_micro_operation += 1
                case 2:
                    computer_state.system_bus.address_bus = (
                        computer_state.system_registers.mar
                    )
                    computer_state.actual_micro_operation += 1
                case 3:
                    computer_state.system_registers.mbr = computer_state.alu.result
                    computer_state.actual_micro_operation += 1
                case 4:
                    computer_state.system_bus.data_bus = (
                        computer_state.system_registers.mbr
                    )
                    computer_state.actual_micro_operation += 1
                case 5:
                    computer_state.data_memory.write(
                        address, computer_state.system_registers.mbr
                    )
                    computer_state.actual_micro_operation = 0
                    computer_state.cycle = CycleState.FETCH_INS
                    computer_state.system_registers.pc = (
                        f"{int(computer_state.system_registers.pc, 2) + 1:04b}"
                    )
