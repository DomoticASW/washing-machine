import threading
from enum import Enum
import time
from pydantic import BaseModel

class MachineState(str, Enum):
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    ERROR = "Error"

class InvalidOperationError(Exception):
    """Exception raised for invalid operations on the washing machine."""
    pass

class WashingProgram(BaseModel):
    name: str
    duration_sec: int

    model_config = {
        "frozen": True
    }

class WashingState(BaseModel):
    state: MachineState
    program: str | None
    remaining_time: int

    model_config = {
        "frozen": True
    }

class WashingMachine:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.state = MachineState.IDLE
        self.current_program = None
        self.remaining_time = 0
        self._thread = None
        self._lock = threading.Lock()

        self.programs = {
            "cotton": WashingProgram(name="Cotton", duration_sec=30),
            "synthetics": WashingProgram(name="Synthetics", duration_sec=20),
            "quickwash": WashingProgram(name="Quick Wash", duration_sec=10)
        }

    def restart_ws(self):
            if self.state in [MachineState.ERROR, MachineState.COMPLETED]:
                with self._lock: 
                    self.state = MachineState.IDLE
                self.current_program = None
                self.remaining_time = 0
                print("Washing machine is now OFF.")
            else:
                raise InvalidOperationError("Cannot power off during a cycle.")

    def start_program(self, program_name: str):
            if self.state != MachineState.IDLE:
                raise InvalidOperationError("Cannot start. Make sure the machine is ON and a program is selected.")
            if program_name == "None":
                raise InvalidOperationError("No program selected. Please choose a valid program.")
            program = self.programs.get(program_name.lower().replace(" ", ""))
            if program:
                self.current_program = program.name
                self.remaining_time = program.duration_sec
                self.start()
                self._thread = threading.Thread(target=self._run_cycle, daemon=True)
                self._thread.start()
                print(f"Program '{program.name}' started.")
            else:
                raise InvalidOperationError(f"Program '{program_name}' not found.")

    def start(self):
        with self._lock:
            self.state = MachineState.RUNNING

    def pause(self):
        if self.state == MachineState.RUNNING:
            with self._lock: 
                self.state = MachineState.PAUSED
            print("Washing paused.")
        else:
            raise InvalidOperationError("Machine is not running.")

    def resume(self):
        if self.state == MachineState.PAUSED:
            with self._lock:
                self.state = MachineState.RUNNING
            print("Resuming wash.")
        else:
            raise InvalidOperationError("Machine is not paused.")

    def status(self):
        return WashingState(
            state=self.state,
            program=self.current_program,
            remaining_time=self.remaining_time
        )
    
    def _run_cycle(self):
        while self.remaining_time > 0:
            if self.state == MachineState.RUNNING:
                self.remaining_time -= 1
                time.sleep(1)

        with self._lock:         
            self.state = MachineState.COMPLETED
            time.sleep(5)
            print(f"Program '{self.current_program}' completed.")
        self.restart_ws()  # Reset the machine after completion