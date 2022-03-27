#!/usr/bin/env python

import os
import pandas_datareader as pdr
import yaml

with open("../secret.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        tiingo_key = data['tiingo_api_key']
    except yaml.YAMLError as exc:
        print(exc)
        exit()

SPY = pdr.get_data_tiingo('SPY', api_key=tiingo_key)