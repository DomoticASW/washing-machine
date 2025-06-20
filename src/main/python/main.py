import os
import uvicorn
from domain.WashingMachine import WashingMachine
from domain.WashingMachineAgent import WashingMachineAgent
from adapters.DomoticASWHttpProtocol import create_server
from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter
from ports.ServerProtocol import ServerAddress

if __name__ == "__main__":
    device_server_port = os.getenv("DEVICE_SERVER_PORT", "8080")
    server_port = os.getenv("SERVER_PORT")
    server = ServerCommunicationProtocolHttpAdapter()
    washing_machine = WashingMachine("WSH001", "Washing Machine 001")
    washing_machine_agent = WashingMachineAgent(
        washing_machine=washing_machine,
        server=server,
        period_sec=1
    )
    # Example usage
    # washing_machine.start_program("quick")
    # time.sleep(5) 
    # washing_machine.pause()
    # time.sleep(2)
    # washing_machine.resume()
    # washing_machine._thread.join()
    app = create_server(washing_machine_agent)
    if(server_port is not None):
        washing_machine_agent.set_server_address(
            ServerAddress("localhost", int(server_port))
        )
        washing_machine_agent.start()
    uvicorn.run(app, host="0.0.0.0", port=int(device_server_port))
