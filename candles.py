import json
import requests
import talib
import numpy as np

from talib import abstract
from config import *

# Initiate our application
def main():
  # Set instrument
  instrument = "EUR_USD"

  # Last candles
  last_ten = get_last_N_candles(instrument, 10)

  last_five = get_last_N_candles(instrument, 5)

  # OHLCVs
  OHLCV10 = get_OHLCV(last_ten)

  OHLCV5 = get_OHLCV(last_five)

# HTTP request to Oanda API to get last N candles
def get_last_N_candles(instrument, n):
  # Must provide authorization for permission
  headers = {"Authorization": "Bearer {}".format(access_token)}

  params = {
    'granularity': 'H1',
    'count': n
  }

  # Send request and store json response
  last_n_candles = requests.get(API_URL + '/v3/instruments/' + instrument + '/candles', headers = headers, params = params).json()['candles']
  return last_n_candles

# Format information to get OHLCV of last 10
def get_OHLCV(last_N_candles):
  OHLCV = {
    'open': [],
    'high': [],
    'low': [],
    'close': [],
    'volume': []
  }

  # Loop through each candle and take O, H, L, C, V and store
  for candle in last_N_candles:
    OHLCV['open'].append(float(candle['mid']['o']))
    OHLCV['high'].append(float(candle['mid']['h']))
    OHLCV['low'].append(float(candle['mid']['l']))
    OHLCV['close'].append(float(candle['mid']['c']))
    OHLCV['volume'].append(float(candle['volume']))

  # Convert all lists to numpy arrays
  for _list in OHLCV:
    OHLCV[_list] = np.asarray(OHLCV[_list])

  return OHLCV

if __name__ == "__main__":
  main()


################################################# DEPRECATED ##########################################################


# from alpha_vantage.foreignexchange import ForeignExchange
# from oandapyV20 import API
# from oandapyV20.exceptions import V20Error


####### ALPHA VANTAGE

# fe = ForeignExchange(key = access_token)
# response = fe.get_currency_exchange_rate('GBP', 'JPY')
# response = response[0]

# currency_info = {
#   'from_currency': response['1. From_Currency Code'].encode('ascii','ignore'),
#   'to_currency': response['3. To_Currency Code'].encode('ascii','ignore'),
#   'exchange_rate': response['5. Exchange Rate'].encode('ascii','ignore')
# }

# print currency_info

###

# getExhangeRate = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=GBP&to_currency=JPY&apikey=" + access_token).json()
# currentRate = getExhangeRate["Realtime Currency Exchange Rate"]

# currency_info = {
#   'from_currency': currentRate['1. From_Currency Code'].encode('ascii','ignore'),
#   'to_currency': currentRate['3. To_Currency Code'].encode('ascii','ignore'),
#   'exchange_rate': currentRate['5. Exchange Rate'].encode('ascii','ignore')
# }
# print(currency_info)

####### OANDA
# from oandapyV20.contrib.factories import InstrumentsCandlesFactory

# client = API(access_token=access_token)

# _from = 10
# _to = 5
# gran = "H1"
# instr = "GBP_JPY"

# params = {
#     "granularity": gran,
#     "from": _from,
#     "to": _to
# }

# def cnv(r, h):
#     for candle in r.get('candles'):
#         ctime = candle.get('time')[0:19]
#         try:
#             rec = "{time},{complete},{o},{h},{l},{c},{v}".format(
#                 time=ctime,
#                 complete=candle['complete'],
#                 o=candle['mid']['o'],
#                 h=candle['mid']['h'],
#                 l=candle['mid']['l'],
#                 c=candle['mid']['c'],
#                 v=candle['volume'],
#             )
#         except Exception as e:
#             print(e, r)
#         else:
#             h.write(rec+"\n")

# with open("/tmp/{}.{}.out".format(instr, gran), "w") as O:
#     for r in InstrumentsCandlesFactory(instrument=instr, params=params):
#         print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
#         rv = client.request(r)
#         cnv(r.response, O)



# from oandapyV20.endpoints import trades

# client = API(access_token=access_token)

# # request trades list
# r = trades.TradesList(ACCOUNT_ID)
# rv = client.request(r)
# print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))






# Exhange Rate
# EMA5
# EMA10
# Stochm
# RSI