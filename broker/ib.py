## Interface with my ib gateway
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
from queue import Queue
import pandas as pd
import threading
import time
import yaml
import logging
import os

# utility functio

def get_account_stocks_df():

    df_details = pd.DataFrame(columns = [
        "Symbol", "SecType", "Exchange", "Position",
        "MarketPrice", "AverageCost", "UnrealizedPNL", "RealizedPNL", "AccountName", "Right", "Strike"
    ])

    return df_details


class IBGateway(EWrapper, EClient):
    '''
    This is the class
    '''
    def __init__(self, queue):
        EClient.__init__(self, self)
        self.queue = queue

    def error(self, reqId, errorCode, errorString):
        logging.error("Error: %s %s %s", reqId, errorCode, errorString)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        logging.info('The next valid order id is: %d', self.nextorderId)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):

        if contract.secType == "OPT": 
            msg = {
                "Type": "UpdatePortfolio",
                "Symbol": contract.symbol,
                "SecType": contract.secType,
                "Exchange": contract.exchange,
                "Position": position,
                "MarketPrice": marketPrice,
                "AverageCost": averageCost,
                "UnrealizedPNL": unrealizedPNL,
                "RealizedPNL": realizedPNL,
                "AccountName": accountName,
                "Strike": contract.strike,
                "Right": contract.right,
            }
        else:
            msg = {
                "Type": "UpdatePortfolio",
                "Symbol": contract.symbol,
                "SecType": contract.secType,
                "Exchange": contract.exchange,
                "Position": position,
                "MarketPrice": marketPrice,
                "AverageCost": averageCost,
                "UnrealizedPNL": unrealizedPNL,
                "RealizedPNL": realizedPNL,
                "AccountName": accountName,
                "Strike": None,
                "Right": None,
            }

        self.queue.put(msg)
        # print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
        #       "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
        #       "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)



    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        msg = {
            "Type": "UpdateAccountValue",
            "Key": key, "Value": val, "Currency": currency, "AccountName": accountName
        }
        self.queue.put(msg)
        #print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    def updateAccountTime(self, timeStamp: str):
        #print("UpdateAccountTime. Time:", timeStamp)
        msg = {
            "Type": "UpdateAccountTime",
            "Time": timeStamp,
        }
        self.queue.put(msg)

    def accountDownloadEnd(self, accountName: str):
        #print("AccountDownloadEnd. Account:", accountName)
        msg = {
            "Type": "AccountDownloadEnd",
            "Account": accountName,
        }
        self.queue.put(msg)

class IB:

    def __init__(self):
        q =  Queue()
        self.app = IBGateway(q) 
        self.connected = False

    def __read_secret(self):
        # read from secret
        secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "secret.yaml")
        with open(secret_path, "r") as stream:
            try:
                data = yaml.safe_load(stream)
                ib_gateway_port = data['ib_gateway_port']
                return ib_gateway_port

            except yaml.YAMLError as exc:
                print(exc)


    def setup_ib_deamon(self):

        #TODO: assume it can completed, but can set a fix retry.
        def run_loop():
            self.app.run()

        try:

            ib_port = self.__read_secret()
            self.app.connect('127.0.0.1', int(ib_port), 123)

            self.app.nextorderId = None

            #Start the socket in a thread
            api_thread = threading.Thread(target=run_loop, daemon=True)
            api_thread.start()

            #Check if the API is connected via orderid
            while True:
                if isinstance(self.app.nextorderId, int):
                    logging.info('connected')
                    self.connected = True
                    break
                else:
                    logging.info('waiting for connection')
                    time.sleep(1)
        except Exception as e:
            print(e)
            self.connected = False

    def close(self):
        self.app.disconnect()

    def get_account_stock(self):

        """ Return a data frame containing fields:
        Symbol, SecType, Exchange, Position, MarketPrice, AverageCost, UnrealizedPNL, RealizedPNL, AccountName
        """

        # Account number can be omitted when using reqAccountUpdates with single account structure
        self.app.reqAccountUpdates(True, "")

        df = get_account_stocks_df()
        # dispatch the message and wait for the result?
        while True:
            try:
                msg = self.app.queue.get()
                msg_type = msg["Type"]

                #print(msg)

                if msg_type == "UpdatePortfolio":
                    
                    df = df.append({"Symbol": msg["Symbol"], "SecType": msg["SecType"], "Exchange": msg["Exchange"], "Position": msg["Position"],
                        "MarketPrice": msg["MarketPrice"], "AverageCost": msg["AverageCost"], "UnrealizedPNL": msg["UnrealizedPNL"], 
                        "RealizedPNL": msg["RealizedPNL"], "AccountName": msg["AccountName"], "Right": msg["Right"], "Strike": msg["Strike"],}, ignore_index=True)

                elif msg_type == "AccountDownloadEnd":
                    break

            except Exception as e :
                # something bad
                print(e)
                break

        return df
        

if __name__ == '__main__':
    ib = IB()

    ib.setup_ib_deamon()

    df = ib.get_account_stock()
    print(df)

    ib.close()


