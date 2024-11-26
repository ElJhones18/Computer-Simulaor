class OpcodesAndTypes:
    # Opcodes (4 bits)
    opcodes = {
        "MOV": "0000",
        "SUB": "0001",
        "MUL": "0010",
        "DIV": "0011",
        "ADD": "0100",
        "JMP": "0101",
        "JZ": "0110",
        "JN": "0111",
    }

    # Tipos de operandos (2 bits)
    TIPO_NUMERO = "00"
    TIPO_REGISTRO = "01"
    TIPO_MEMORIA = "10"
    TIPO_ETIQUETA = "11"
