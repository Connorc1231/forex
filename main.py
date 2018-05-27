from candles import *
from indicators import *

def main():
  instrument = 'EUR_USD'
  n = 10
  candles = get_last_N_candles(instrument, n)
  OHLCV = get_OHLCV(candles)
  

  SMA = getSMA(OHLCV['close'])
  print(SMA)

  


if __name__ == "__main__":
  main()