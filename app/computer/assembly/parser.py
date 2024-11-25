import streamlit as st
from computer.assembly.opcodes_and_types import OpcodesAndTypes


class Parser:
    def __init__(self):
        # Diccionario de códigos de operación
        self.opcodes = OpcodesAndTypes.opcodes
        self.TIPO_NUMERO = OpcodesAndTypes.TIPO_NUMERO
        self.TIPO_REGISTRO = OpcodesAndTypes.TIPO_REGISTRO
        self.TIPO_MEMORIA = OpcodesAndTypes.TIPO_MEMORIA
        self.TIPO_ETIQUETA = OpcodesAndTypes.TIPO_ETIQUETA

        self.labels = {}
        self.current_address = 0

    def is_number(self, token):
        try:
            int(token)
            return True
        except ValueError:
            return False

    def is_register(self, token):
        if not token.startswith("R"):
            return False
        try:
            reg_num = int(token[1:])
            return 1 <= reg_num <= 4  # 4 registros disponibles
        except ValueError:
            return False

    def is_memory(self, token):
        if not token.startswith("#"):
            return False
        try:
            addr = int(token[1:])
            return 0 <= addr < 16  # 4 bits permiten hasta 16 posiciones
        except ValueError:
            return False

    def encode_operand(self, operand, allow_label=False):
        """Convierte un operando a su representación binaria incluyendo tipo"""
        if self.is_number(operand):
            value = int(operand)
            if not (0 <= value < 16):  # 4 bits para valor
                raise ValueError(f"Número {value} fuera de rango (0-15)")
            return self.TIPO_NUMERO + format(value, "04b")

        elif self.is_register(operand):
            reg_num = int(operand[1:])
            return self.TIPO_REGISTRO + format(reg_num, "04b")

        elif self.is_memory(operand):
            addr = int(operand[1:])
            return self.TIPO_MEMORIA + format(addr, "04b")

        elif allow_label and operand in self.labels:
            addr = self.labels[operand]
            return self.TIPO_ETIQUETA + format(addr, "04b")

        else:
            raise ValueError(f"Operando inválido: {operand}")

    def first_pass(self, program):
        """Primer paso: recolectar las etiquetas y sus direcciones"""
        lines = program.split("\n")
        address = len(st.session_state.computer_state.program_memory.get_all())

        for line in lines:
            line = line.strip()
            if not line or line.startswith(";"):
                continue

            if ":" in line:
                label, rest = line.split(":", 1)
                label = label.strip()
                self.labels[label] = address
                line = rest.strip()
                if not line:
                    continue

            address += 1

    def parse_instruction(self, line):
        """Parsea una línea de instrucción y retorna su codificación binaria"""
        if ";" in line:
            line = line.split(";")[0]

        tokens = line.strip().split()

        if not tokens:
            return None

        opcode = tokens[0].upper()
        if opcode not in self.opcodes:
            raise ValueError(f"Código de operación inválido: {opcode}")

        binary = self.opcodes[opcode]

        # Procesar operandos según el tipo de instrucción
        if opcode in ["JMP", "JZ", "JN"]:
            if len(tokens) != 2:
                raise ValueError(f"Instrucción {opcode} requiere una etiqueta")
            binary += self.encode_operand(
                tokens[1], allow_label=True
            )  # Permite etiquetas
            binary += self.TIPO_NUMERO + "0000"  # Segundo operando no usado
        else:
            if len(tokens) != 3:
                raise ValueError(f"Instrucción {opcode} requiere dos operandos")
            op1 = self.encode_operand(tokens[1])
            if op1[:2] == "00":
                raise ValueError(f"Operando 1 debe ser un registro o dirección")
            binary += self.encode_operand(tokens[1])
            binary += self.encode_operand(tokens[2])

        return binary

    def parse_program(self, program):
        """Parsea un programa completo y retorna lista de instrucciones en binario"""
        self.first_pass(program)
        binary_instructions = []

        for line in program.split("\n"):
            line = line.strip()
            if not line or line.startswith(";"):
                continue

            if ":" in line:
                label, rest = line.split(":", 1)
                line = rest.strip()
                if not line:
                    continue

            binary = self.parse_instruction(line)
            if binary:
                binary_instructions.append(binary)

        # print(self.labels)

        return binary_instructions
