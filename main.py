from candles import *
from indicators import *

# NOTE
# RSI and EMA are smoothed, meaning they depend on previous values of themselves
# Currently using static data, can only get first point of RSI / EMA
# Once implement stream and real-time, can store RSI / EMA in db and use for smoothing


def main():
  instrument = 'EUR_USD'
  # RSI requires one inital datapoint BEFORE its timeperiod, n = 15 for RSI14
  n = 15
  candles = get_last_N_candles(instrument, n)
  OHLCV = get_OHLCV(candles)
  closes = OHLCV['close']

  SMA = getSMA(closes)
  # print(SMA)

  mult = getMultiplier(n)
  # print(mult)
  EMA = getEMA(closes[-1], SMA, mult)
  # print(EMA)


  avgGainLoss = getAvgGainLoss(closes)
  RS = getRS(avgGainLoss)
  print(RS)
  RSI = getRSI(RS)
  print(RSI)

if __name__ == "__main__":
  main()