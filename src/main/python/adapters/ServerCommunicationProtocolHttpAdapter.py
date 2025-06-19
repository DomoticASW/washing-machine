import httpx
from domain.WashingMachine import WashingState
from ports import ServerProtocol
from ports.ServerProtocol import ServerCommunicationProtocol

class ServerCommunicationProtocolHttpAdapter(ServerCommunicationProtocol):
  async def send_event(self, server_address: ServerProtocol.ServerAddress, event, washing_machine_id: str) -> None:
    print(f"CLIENT: Sending event for washing machine {washing_machine_id} at {server_address.host}:{server_address.port}")
    async with httpx.AsyncClient() as client:
      await client.post(f"http://{server_address.host}:{server_address.port}/api/devices/{washing_machine_id}/events",
                              json=event)
  
  async def update_state(self, server_address: ServerProtocol.ServerAddress, state: WashingState, washing_machine_id: str) -> None:
    print(f"CLIENT: Updating state for washing machine {washing_machine_id} at {server_address.host}:{server_address.port}")
    async with httpx.AsyncClient() as client:
      await client.patch(f"http://{server_address.host}:{server_address.port}/api/devices/{washing_machine_id}/properties",
                              json=state.model_dump())
  
    

