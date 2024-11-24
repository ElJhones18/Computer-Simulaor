from dataclasses import dataclass


@dataclass
class SystemRegisters:
    pc: str = "0000"
    ir: str = "0000"
    mar: str = "0000"
    mbr: str = "0000"
