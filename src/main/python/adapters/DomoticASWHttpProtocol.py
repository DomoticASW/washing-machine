from fastapi import Body, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from domain.WashingMachine import InvalidOperationError, WashingMachine
from domoticASW.domoticASWProtocol import ActionId, DeviceAction, DevicePropertyWithSetter, DevicePropertyWithTypeConstraint, DeviceRegistration, Type, TypeConstraintEnum, TypeConstraintNone
from domain import WashingMachineAgent
from ports.ServerProtocol import ServerAddress

def OkResponse(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": message}
    )

def BadRequest(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": message}
    )

def NotFound(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": message}
    )

# === ENDPOINTS ===

def create_server(washing_machine_agent: WashingMachineAgent) -> FastAPI:
    app = FastAPI()

    def get_washing_machine_agent() -> WashingMachineAgent:
        return washing_machine_agent
    
    @app.get("/check-status")
    def check_status():
        return OkResponse(message="Washing machine is online")

    @app.post("/execute/{action}")
    def execute_action(action: str, body: dict = Body(...), machine_agent: WashingMachineAgent = Depends(get_washing_machine_agent)):
        machine = machine_agent.washing_machine
        try:
            match action:
                case "start_program":
                    machine.start_program(body.get("input"))
                case "pause":
                    machine.pause()
                case "resume":
                    machine.resume()
                case "restart_ws":
                    machine.restart_ws()
                case _:
                    return NotFound(message=f"Action '{action}' not found")
        except InvalidOperationError as e:
            return BadRequest(message=str(e))
        return OkResponse(message=f"Action '{action}' executed successfully")

    @app.post("/register")
    def register_device(request: Request, body: dict = Body(...),machine_agent: WashingMachineAgent = Depends(get_washing_machine_agent)):
        server_host = "localhost"
        server_port = body.get("server")
        machine_agent.set_server_address(ServerAddress(server_host, server_port))
        print(f"SERVER: Machine agent start to run")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=deviceRegistration(machine_agent.washing_machine).model_dump()
        )
    
    return app


def deviceRegistration(washing_machine: WashingMachine) -> DeviceRegistration:
    return DeviceRegistration(
        id=washing_machine.id,
        name=washing_machine.name,
        properties=[
            DevicePropertyWithTypeConstraint(
                id="state",
                name="State",
                value=washing_machine.state.name,
                typeConstraints=TypeConstraintEnum(values=["Idle", "Running", "Paused", "Completed", "Error"])
            ),
            DevicePropertyWithSetter(
                id="program",
                name="Program",
                value="None",
                setterActionId=ActionId("start_program")
            ),
            DevicePropertyWithTypeConstraint(
                id="remaining_time",
                name="Remaining Time",
                value=washing_machine.remaining_time,
                typeConstraints=TypeConstraintNone(type=Type.INT)
            )
        ],
        actions=[
            DeviceAction(
                id="start_program",
                name="Start Program",
                description="Starts the selected washing program.",
                inputTypeConstraints=TypeConstraintEnum(values=["Cotton", "Synthetics", "Quick Wash"])
            ),
            DeviceAction(
                id="pause",
                name="Pause Washing Machine",
                description="Pauses the current washing cycle.",
                inputTypeConstraints=TypeConstraintNone(type=Type.VOID)
            ),
            DeviceAction(
                id="resume",
                name="Resume Washing Machine",
                description="Resumes the paused washing cycle.",
                inputTypeConstraints=TypeConstraintNone(type=Type.VOID)
            ),
            DeviceAction(
                id="restart_ws",
                name="Restart Washing Machine",
                description="Restarts the washing machine.",
                inputTypeConstraints=TypeConstraintNone(type=Type.VOID)
            )
        ],
        events=["start", "stop", "program_completed"]
    )
