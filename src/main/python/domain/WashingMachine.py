import threading
from enum import Enum, auto
import time

class MachineState(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    ERROR = auto()

class InvalidOperationError(Exception):
    """Exception raised for invalid operations on the washing machine."""
    pass

class WashingProgram:
    def __init__(self, name, duration_sec):
        self.name = name
        self.duration_sec = duration_sec

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
            "cotton": WashingProgram("Cotton", 30),
            "synthetics": WashingProgram("Synthetics", 20),
            "quick": WashingProgram("Quick Wash", 10)
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
            program = self.programs.get(program_name.lower())
            if program:
                self.current_program = program
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
        return {
            "state": self.state.name,
            "program": self.current_program.name if self.current_program else None,
            "remaining_time": self.remaining_time
        }
    
    def _run_cycle(self):
        while self.remaining_time > 0:
            if self.state == MachineState.RUNNING:
                print(f"Time remaining: {self.remaining_time:.0f}s")
                self.remaining_time -= 1
                time.sleep(1)

        with self._lock:         
            self.state = MachineState.COMPLETED
            print(f"Program '{self.current_program.name}' completed.")
        self.restart_ws()  # Reset the machine after completion