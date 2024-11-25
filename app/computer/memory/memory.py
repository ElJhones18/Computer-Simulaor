from typing import List, Tuple


class Memory:
    def __init__(self, size: int, type: str = "data"):
        if type == "data":
            self.memory: List[Tuple[str, str]] = [(f"{i:04b}", "0000000000000000") for i in range(size)]
        elif type == "program":
            self.memory: List[Tuple[str, str]] = [(f"{i + size:04b}", "0000000000000000") for i in range(size)]
            
    def get_all(self) -> List[Tuple[str, str]]:
        return self.memory

    def read(self, address: str) -> str:
        for addr, value in self.memory:
            if addr == address:
                return value

    def write(self, address: str, value: str):
        for i, (addr, _) in enumerate(self.memory):
            if addr == address:
                self.memory[i] = (address, value)
                break
