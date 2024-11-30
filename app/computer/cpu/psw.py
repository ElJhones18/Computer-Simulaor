from dataclasses import dataclass


@dataclass
class PSW:
    zero: bool = False
    negative: bool = False
    interrupt: bool = False
    overflow: bool = False

    def update_flags(self, result: int):
        self.zero = result == 0
        self.negative = result < 0
