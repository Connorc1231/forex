from candles import *
from indicators import *

# NOTE
# RSI and EMA are smoothed, meaning they depend on previous values of themselves
# Currently using static data, can only get first point of RSI / EMA
# Once implement stream and real-time, can store RSI / EMA in db and use for smoothing


def main():
  instrument = 'EUR_USD'
  # RSI requires one inital datapoint BEFORE its timeperiod, n = 15 for RSI14
  n =500 
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
  RSIs = []
  prevAvgGainLoss = getAvgGainLoss(closes[0 : 15])
  print(prevAvgGainLoss)
  for index, price in enumerate(closes):
    if index == len(closes) - 14:
      break
    else:
      if index == 0:
        firstRS = calcFirstRS(prevAvgGainLoss)
        firstRSI = calcRSI(firstRS)
        RSIs.append(firstRSI)
      else:
        currGainLoss = closes[index + 14] - closes[index + 13]
        smoothedRS = calcSmoothedRS(currGainLoss, prevAvgGainLoss)

        # Trouble correctly updating prevAvgGainLoss correctly
        if currGainLoss > 0:
          prevAvgGainLoss['gain'] = (prevAvgGainLoss['gain'] * 13 + currGainLoss) / 14
          prevAvgGainLoss['loss'] = (prevAvgGainLoss['loss'] * 13) / 14
        else:
          prevAvgGainLoss['gain'] = (prevAvgGainLoss['gain'] * 13) / 14 
          prevAvgGainLoss['loss'] = (prevAvgGainLoss['loss'] * 13 + abs(currGainLoss)) / 14
        RSI = calcRSI(smoothedRS)
        RSIs.append(RSI)

  print(RSIs)
  return RSIs


if __name__ == "__main__":
  main()