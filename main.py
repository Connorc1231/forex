from candles import *
from indicators import *

# NOTE
# RSI and EMA are smoothed, meaning they depend on previous values of themselves
# Currently using static data, can only get first point of RSI / EMA
# Once implement stream and real-time, can store RSI / EMA in db and use for smoothing


def main():
  instrument = 'EUR_USD'
  # RSI requires one inital datapoint BEFORE its timeperiod, n = 15 for RSI14
  n = 2000 
  candles = get_last_N_candles(instrument, n)
  OHLCV = get_OHLCV(candles)
  closes = OHLCV['close']

  #### GET SMA ####
  SMA = getSMA(closes)
  # print(SMA)

  #### GET EMA ####
  EMAs = getEMA(closes)

  #### GET RSI ####
  RSIs = getRSI(closes)

  #### GET RSI #####
  # avgGainLoss = getAvgGainLoss(closes)
  # RS = getRS(avgGainLoss)
  # print(RS)
  # RSI = getRSI(RS)
  # print(RSI)

def getEMA(closes):
  EMAs = []
  for index, price in enumerate(closes):
    dataChunk = closes[index : index + 10]
    if index == len(closes) - 9:
      break
    else:
      if index == 0:
        firstSMA = getSMA(closes[0 : 10])
        EMAs.append(firstSMA)
      else:
        prevEMA = EMAs[-1]
        currEMA = calcEMA(closes[index + 9], prevEMA, getMultiplier(10))
        EMAs.append(currEMA)
    return EMAs

def getRSI(closes):
  closes = [46.125, 47.125, 46.4375, 46.9375, 44.9375, 44.25, 44.625, 45.75, 47.8125, 47.5625, 47, 44.5625, 46.3125, 47.6875, 46.6875, 45.6875, 43.0625, 43.5625, 44.875, 43.6875]
  RSIs = []
  prevAvgGainLoss = getAvgGainLoss(closes[0 : 15])
  for index, price in enumerate(closes):
    if index == len(closes) - 14:
      break
    else:
      if index == 0:
        firstRS = calcFirstRS(prevAvgGainLoss)
        firstRSI = calcRSI(firstRS)
        RSIs.append(firstRSI)
      else:
        currGainLoss = round(closes[index + 14] - closes[index + 13], 4)
        if currGainLoss > 0:
          prevAvgGainLoss['gain'] += (prevAvgGainLoss['gain'] * 13 + currGainLoss) / 14 
        else:
          prevAvgGainLoss['loss'] += abs((prevAvgGainLoss['loss'] * 13 + currGainLoss) / 14 )
        smoothedRS = calcSmoothedRS(currGainLoss, prevAvgGainLoss)
        RSI = calcRSI(smoothedRS)
        RSIs.append(RSI)

  print(RSIs)
  return RSIs


if __name__ == "__main__":
  main()