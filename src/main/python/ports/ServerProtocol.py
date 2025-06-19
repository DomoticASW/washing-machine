from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.WashingMachine import WashingState

@dataclass(frozen=True)
class ServerAddress():
    host: str
    port: int

class ServerCommunicationProtocol(ABC):
    @abstractmethod
    async def send_event(self, server_address: ServerAddress, event, washing_machine_id: str):
        pass

    @abstractmethod
    async def update_state(self, server_address: ServerAddress, state: WashingState, washing_machine_id: str):
        pass