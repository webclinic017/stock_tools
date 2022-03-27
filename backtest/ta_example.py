import talib
import os
import sys, importlib
from pathlib import Path

# Relative import have been difficult
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3

def import_parents(level=1):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]
    
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__) # won't be needed after that

if __name__ == '__main__' and __package__ is None:
    import_parents(level=2) # N = 3

import numpy
from ..data_api.stock import get_olhc
import datetime

if __name__ == '__main__':

    date_from = datetime.date(2021, 12, 1)
    date_to = datetime.date(2022, 1, 10)

    res = get_olhc('AAPL', date_from, date_to, 'US')

    atr = talib.ATR(res["High"], res["Low"], res["Close"], timeperiod=14)

    print(atr)