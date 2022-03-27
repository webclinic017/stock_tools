import yaml
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta
import pandas as pd

#https://api.pancakeswap.info/api/v2/tokens/0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82

#popcoin is on bnb chain
# pancake swap is on BSC chain.
#Cheaper and faster than Uniswap? Discover PancakeSwap, the leading DEX on Binance Smart Chain (BSC) with the best farms in DeFi and a lottery for CAKE.

# can only get the latest price, not more.

def __get_bsc_contract_address(symbol: str):
    cypto_address = {
        'bnb': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
        'ceek': '0x55d398326f99059fF775485246999027B3197955',
        'avax-x': '0x1CE0c2827e2eF14D5C4f29a091d735A204794041', 
        'sol': '0x570A5D26f7765Ecb712C0924E4De545B89fD43dF',
        'btc': '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c',
        'eth': '0x2170Ed0880ac9A755fd29B2688956BD959F933F8',
    }

    return cypto_address.get(symbol.lower())


def get_olhc(symbol: str):

    contract_address = __get_bsc_contract_address(symbol)
    url = "https://api.pancakeswap.info/api/v2/tokens/%s" % contract_address
    session = Session()

    try:
        response = session.get(url)
        data = json.loads(response.text)
        print(data)

        # download and save it to other place

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        raise

if __name__ == '__main__':
    get_olhc('ceek')