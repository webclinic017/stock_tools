# To backtest and try on ByBit for me. so that I at least have some stop loss.

## Introduction of strategy

Here is a list of strategy I read from the web. and I want to implement

## Technology stack

Not much 

    * Python
    * Docker and K8s
    * CCXT
    * Backtrader (Seems only bug-fix now) and backtrader-ccxt (seems only bug-fix now)
    * ByBit
    * Binance

## Test data

    Here are some crypto I want to do test on, they are ranked high on coinmarketcap.com[1] and some recent coin from news.

    Data captured as of 26 March


|coin   | rank  | description |
|---|---|---|
| Bitcoin  | 1  |   |
| Ethereum  | 2  |   |
| BNB | 4  | from binance |
| XRP  | 6  | lawsuit? |
| Cardano (ADA)  | 7  |  etherum of japan |
| Solana  | 8   | mainly in NFT  |
| Terra (LUNA)  | 9  | alog stable coin  |
| Avalanche (AVAX)  | 10  | new eth  |
| Polkadot (DOT)  | 11  | cross chain?  |
| Dogecoin (DOGE)  | 12 | meme coin  |
| Polygon (MATIC)  | 16  | cheaper nft  |
| Cosmos (ATOM)  | 22 | zone? |
| Waves  | 45 | russia chain  |
| ApeCoin | 39 | BYAC  |
| Cronos (CRO) | 18 | crypto.com credit card |

## Backtest strategy

    Here is the strategy I want to implement.

    * MACD
    * RSI
    * SAR
    * MFI
    * Boillinger Band
    * GMMA

    I also present a simple future trading stop loss bot to update stop loss according to daily high price and ATR.

## Brokers

    * Binance
        
        Assume regular user

        Spot Commission: (0.1%)

        Future Commission (USDT): (0.04% Taker, 0.02% Maker)

        Future Commission (BUSD): (0.036% Taker, 0.018% Maker)

    * Bybit

        Source: https://help.bybit.com/hc/zh-tw/articles/360039261154-交易手續費

        Spot Commission: (Taker: 0.1% + Maker: 0.1%)

        Future Commission: (Taker: 0.06% + Maker: 0.01%)

## Result

    Here I present the result of my code and what I think is my current best strategy.

    ...


## Reference

[1] [CoinMarketCap.com](https://coinmarketcap.com)

[2] [Youtube - partime larry channel](https://www.youtube.com/c/parttimelarry)

[3] [Youtube - 老貓與指標](https://www.youtube.com/c/老貓與指標)

[4] Binance API: https://binance.zendesk.com/hc/en-us/articles/115000878605-API-Reference-Guide

[5] Binance fee: https://www.binance.com/en/fee

[6] Bybit API: https://bybit.com/api/v1/docs

[7] ByBit fee: https://help.bybit.com/hc/zh-tw/articles/360039261154-交易手續費