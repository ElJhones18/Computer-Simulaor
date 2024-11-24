from dataclasses import dataclass


@dataclass
class UserRegisters:
    R1: str = "0000"
    R2: str = "0000"
    R3: str = "0000"
    R4: str = "0000"

    def get_register(self, reg_name: str) -> str:
        return getattr(self, reg_name.lower())

    def set_register(self, reg_name: str, value: str):
        setattr(self, reg_name.lower(), value)
