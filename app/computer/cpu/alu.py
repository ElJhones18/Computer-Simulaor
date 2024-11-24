from dataclasses import dataclass


@dataclass
class ALU:
    operator1: str = "0000"
    operator2: str = "0000"
    operation: str = "+"
    result: str = "0000"

    def execute_operation(self):
        op1 = int(self.operator1, 16)
        op2 = int(self.operator2, 16)

        if self.operation == "+":
            result = op1 + op2
        elif self.operation == "-":
            result = op1 - op2

        self.result = f"{result:04X}"
        return result
