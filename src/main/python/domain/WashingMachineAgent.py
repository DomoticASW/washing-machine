import asyncio
from enum import Enum
from threading import Thread
import threading
import time
from pydantic import BaseModel

from domain.WashingMachine import MachineState, WashingMachine
from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter
from ports.ServerProtocol import ServerAddress

class Event(str, Enum):
    PAUSE = "pause"
    RESUME = "resume"
    COMPLETED = "completed"

class WashingMachineAgent(Thread):
  _server_address: ServerAddress
  def __init__(self, washing_machine: WashingMachine, server: ServerCommunicationProtocolHttpAdapter, server_broadcast_address: ServerAddress, device_port: int,period_sec=1):
    super().__init__(daemon=True)
    self.loop = asyncio.new_event_loop()
    threading.Thread(target=self.loop.run_forever, daemon=True).start()
    self._stop = False
    self.washing_machine = washing_machine
    self.server = server
    self._server_address = None
    self.server_broadcast_address = server_broadcast_address
    self.device_port = device_port
    self.period_sec = period_sec
    self._last_state = None

  def stop(self):
    self._stop = True

  def run(self):
    print(f"AGENT: Starting agent for washing machine {self.washing_machine.id} with period {self.period_sec} seconds")
    while not self._stop:
      time.sleep(self.period_sec)
      if self._server_address is not None:
        status = self.washing_machine.status()
        if self._has_meaningful_change(status.state):
          print(f"AGENT: EVENT!!: {status.state}, Program: {status.program if status.program else 'None'}, Remaining time: {status.remaining_time} seconds")
          future = asyncio.run_coroutine_threadsafe(self.server.send_event(self._server_address, self._build_event(status.state), self.washing_machine.id), self.loop)
          try: 
            future.result()
          except Exception as e:
            print(f"AGENT ERROR! Errore nell'invio dell'evento' {e}")  # Only for debugging purposes
        for property_name, property_value in status.model_dump().items():
          if isinstance(property_value, BaseModel): # If the property is a BaseModel, we need to convert it to a dict
            property_value = property_value.model_dump()
          future = asyncio.run_coroutine_threadsafe(self.server.update_state(self._server_address, property_name, property_value, self.washing_machine.id), self.loop)
          try: 
            future.result()
          except Exception as e:
            print(f"AGENT ERROR! Errore nell'aggiornamento dello stato {e}")
        self._last_state = status.state
      else:
        print(f"AGENT: Sending broadcast announcement")
        asyncio.run_coroutine_threadsafe(
              self.server.announce(self.server_broadcast_address, self.device_port, self.washing_machine.id, self.washing_machine.name), 
              self.loop
          )

  def _has_meaningful_change(self, current_state: MachineState) -> bool:
    print(f"AGENT: Checking for meaningful change: Last state: {self._last_state}, Current state: {current_state}")
    if self._last_state is not current_state and (
              (current_state in [MachineState.PAUSED, MachineState.COMPLETED]) or 
              (self._last_state == MachineState.PAUSED and current_state == MachineState.RUNNING)):
      return True
    else:
      return False
    
  def _build_event(self, state: MachineState) -> Event | None:
    if state == MachineState.PAUSED:
      return Event.PAUSE
    elif state == MachineState.RUNNING:
      return Event.RESUME
    elif state == MachineState.COMPLETED:
      return Event.COMPLETED
    else:
      return None
    
  def set_server_address(self, server_address: ServerAddress):
    print(f"AGENT: Device registered with address: {server_address.host}:{server_address.port}")
    self._server_address = server_address