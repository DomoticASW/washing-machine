from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class ServerAddress():
    host: str
    port: int

@dataclass(frozen=True)
class BroadcastMessage():
    id: str
    name: str
    port: int

class ServerCommunicationProtocol(ABC):
    @abstractmethod
    async def send_event(self, server_address: ServerAddress, event, washing_machine_id: str):
        pass

    @abstractmethod
    async def update_state(self, server_address: ServerAddress, property_name: str, property_value, washing_machine_id: str):
        pass

    @abstractmethod
    async def announce(self, discovery_broadcast_address: ServerAddress, device_port: int, washing_machine_id: str, washing_machine_name: str) -> None:
        pass