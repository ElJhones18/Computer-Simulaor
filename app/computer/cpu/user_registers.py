from dataclasses import dataclass


@dataclass
class UserRegisters:
    R1: str = "0000000000000000"
    R2: str = "0000000000000000"
    R3: str = "0000000000000000"
    R4: str = "0000000000000000"

    def get_register(self, reg_name: str) -> str:
        return getattr(self, reg_name.upper())

    def set_register(self, reg_name: str, value: str):
        if reg_name.upper() in ["R1", "R2", "R3", "R4"]:
            setattr(self, reg_name.upper(), value)
        else:
            raise ValueError(f"Register {reg_name} does not exist.")
