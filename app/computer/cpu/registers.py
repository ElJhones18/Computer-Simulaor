from dataclasses import dataclass


@dataclass
class SystemRegisters:
    pc: str = "1000"
    ir: str = "0000"
    mar: str = "0000"
    mbr: str = "0000"
