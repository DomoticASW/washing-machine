import uvicorn
from domain.WashingMachine import WashingMachine
from domain.WashingMachineAgent import WashingMachineAgent
from adapters.DomoticASWHttpProtocol import create_server
from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter

if __name__ == "__main__":
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
    uvicorn.run(app, host="0.0.0.0", port=8080)
