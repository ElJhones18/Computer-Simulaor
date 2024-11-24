import streamlit as st
class Parser:
    def __init__(self):
        # Diccionario de códigos de operación
        self.opcodes = {
            "ADD": "0000",
            "SUB": "0001",
            "MUL": "0010",
            "DIV": "0011",
            "MOV": "0100",
            "JMP": "0101",
            "JZ": "0110",
            "JN": "0111",
        }

        # Tipos de operandos (2 bits)
        self.TIPO_NUMERO = "00"
        self.TIPO_REGISTRO = "01"
        self.TIPO_MEMORIA = "10"
        self.TIPO_ETIQUETA = "11"

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
