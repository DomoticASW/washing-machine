import os
import uvicorn
from domain.WashingMachine import WashingMachine
from domain.WashingMachineAgent import WashingMachineAgent
from adapters.DomoticASWHttpProtocol import create_server
from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter
from ports.ServerProtocol import ServerAddress

if __name__ == "__main__":
    device_server_port = os.getenv("PORT", "8091")
    server_port = os.getenv("SERVER_PORT", None)
    server_broadcast_port = os.getenv("SERVER_DISCOVERY_PORT",  "30000")
    server_broadcast_host = os.getenv("SERVER_DISCOVERY_ADDR", "255.255.255.255")
    server_broadcast_address = ServerAddress(server_broadcast_host, int(server_broadcast_port))
    server = ServerCommunicationProtocolHttpAdapter()
    ws_id = os.getenv("ID", "WSH001")
    ws_name = os.getenv("NAME", "Washing Machine 001")
    washing_machine = WashingMachine(ws_id, ws_name)
    washing_machine_agent = WashingMachineAgent(
        washing_machine=washing_machine,
        server=server,
        server_broadcast_address=server_broadcast_address,
        device_port=int(device_server_port),
        period_sec=1
    )
    app = create_server(washing_machine_agent)
    if(server_port is not None and server_port != ""):
        print("Server: ", server_port)
        washing_machine_agent.set_server_address(
            ServerAddress("localhost", int(server_port))
        )
    washing_machine_agent.start()
    uvicorn.run(app, host="0.0.0.0", port=int(device_server_port))
