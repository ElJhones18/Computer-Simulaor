from dataclasses import dataclass


@dataclass
class ALU:
    operator1: str = "0000"
    operator2: str = "0000"
    operation: str = "+"
    result: str = "0000000000000000"

    def execute_operation(self):
        op1 = int(self.operator1, 2)
        op2 = int(self.operator2, 2)

        if self.operation == "+":
            result = op1 + op2
        elif self.operation == "-":
            result = op1 - op2
            if result < 0:
                result = 0
        elif self.operation == "*":
            result = op1 * op2
        elif self.operation == "/":
            if op2 != 0:
                result = op1 // op2
            else:
                raise ValueError("División por cero no permitida.")
        else:
            raise ValueError("Operación no válida.")

        self.result = f"{result:b}".zfill(16)
        return result
