import uvicorn
import time
from domain.WashingMachine import WashingMachine
from adapters.DomoticASWHttpProtocol import create_server

if __name__ == "__main__":
    washing_machine = WashingMachine("WSH001", "Washing Machine 001")
    # Example usage
    # washing_machine.start_program("quick")
    # time.sleep(5) 
    # washing_machine.pause()
    # time.sleep(2)
    # washing_machine.resume()
    # washing_machine._thread.join()
    app = create_server(washing_machine)
    uvicorn.run(app, host="0.0.0.0", port=8080)
