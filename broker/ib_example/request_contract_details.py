from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
import threading
import time


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)


    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails, "\n")

    def contractDetailsEnd(self, reqId):
        print("\ncontractDetails End\n")

'''
    def start(self):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "202201"  # June 2020

        self.reqContractDetails(1, contract)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    app = TestApp()
    app.nextOrderId = 0
    app.connect("127.0.0.1", 7497, 123)

    Timer(10, app.stop).start()
    app.run()


if __name__ == "__main__":
    main()

'''

def run_loop():
    app.run()

app = TestApp()
app.connect('127.0.0.1', 7497, 123)

app.nextorderId = None

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

#Check if the API is connected via orderid
while True:
    if isinstance(app.nextorderId, int):
        print('connected')
        print()
        break
    else:
        print('waiting for connection')
        time.sleep(1)

#Create order object
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202201"  # June 2020

app.reqContractDetails(1, contract)
time.sleep(4)

app.disconnect()