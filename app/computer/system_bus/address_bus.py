from dataclasses import dataclass


@dataclass
class SystemBus:
    address_bus: str = "0000"
    data_bus: str = "0000"
    control_bus: str = "0000"