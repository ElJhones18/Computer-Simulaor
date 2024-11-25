from dataclasses import dataclass, field

from computer.system_bus.address_bus import SystemBus
from computer.cpu.alu import ALU
from computer.cpu.psw import PSW
from computer.cpu.registers import SystemRegisters
from computer.cpu.user_registers import UserRegisters
from computer.cycle_state import CycleState
from computer.memory.memory import Memory


@dataclass
class ComputerState:
    cycle: CycleState = CycleState.WAITING
    alu: ALU = field(default_factory=ALU)
    system_registers: SystemRegisters = field(default_factory=SystemRegisters)
    psw: PSW = field(default_factory=PSW)
    user_registers: UserRegisters = field(default_factory=UserRegisters)
    system_bus: SystemBus = field(default_factory=SystemBus)
    data_memory: Memory = field(default_factory=lambda: Memory(8, "data"))
    program_memory: Memory = field(default_factory=lambda: Memory(8, "program"))
    actual_micro_operation: int = 0
    actual_insstruction: str = ""