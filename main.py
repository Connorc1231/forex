from candles import *
from indicators import *

# NOTE
# RSI and EMA are smoothed, meaning they depend on previous values of themselves
# Currently using static data, can only get first point of RSI / EMA
# Once implement stream and real-time, can store RSI / EMA in db and use for smoothing


def main():
  instrument = 'EUR_USD'
  bigDataCloses = get_OHLCV(get_last_N_candles(instrument, 250))['close']

  closes14 = bigDataCloses[0 : 15]
  closes40 = bigDataCloses[0 : 41]
  closes250 = bigDataCloses

  #### GET SMA ####
  SMA = calcSMA(closes14)

  #### GET EMA ####
  EMAList = getEMA(closes14)
  currentEMA = EMAList[-1]

  closes250 = get_OHLCV(get_last_N_candles(instrument, 250))['close']

  #### GET RSI ####
  RSIList = getRSI(closes250)
  currentRSI = RSIList[-1]

  #### GET STOCH ####
  stochList = getStoch(closes250)
  currentStoch = stochList[-1]

  closes40 = get_OHLCV(get_last_N_candles(instrument, 40))['close']
  #### GET BBANDS ####
  BBands = getBBands(closes40)
  currentBBands = {
    'upper': BBands['upper'][-1],
    'mid': BBands['mid'][-1],
    'lower': BBands['lower'][-1]
  }

  indicators = {
    'SMA': SMA,
    'EMA': currentEMA,
    'RSI': currentRSI,
    "Stoch": currentStoch,
    "BBands": currentBBands
  }

  print(indicators)
  return indicators

def getEMA(closes):
  EMAs = []
  for index, price in enumerate(closes):
    dataChunk = closes[index : index + 10]
    if index == len(closes) - 9:
      break
    else:
      if index == 0:
        firstSMA = calcSMA(closes[0 : 10])
        EMAs.append(firstSMA)
      else:
        prevEMA = EMAs[-1]
        currEMA = calcEMA(closes[index + 9], prevEMA, getMultiplier(10))
        EMAs.append(currEMA)
    return EMAs

def getRSI(closes):
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
        currGainLoss = closes[index + 14] - closes[index + 13]
        smoothedRS = calcSmoothedRS(currGainLoss, prevAvgGainLoss)

        if currGainLoss > 0:
          prevAvgGainLoss['gain'] = (prevAvgGainLoss['gain'] * 13 + currGainLoss) / 14
          prevAvgGainLoss['loss'] = (prevAvgGainLoss['loss'] * 13) / 14
        else:
          prevAvgGainLoss['gain'] = (prevAvgGainLoss['gain'] * 13) / 14 
          prevAvgGainLoss['loss'] = (prevAvgGainLoss['loss'] * 13 + abs(currGainLoss)) / 14
        RSI = calcRSI(smoothedRS)
        RSI = round(RSI, 4)
        RSIs.append(RSI)
  return RSIs

def getStoch(closes):
  kList = []
  for index, price in enumerate(closes):
    closeChunk = closes[index : index + 14]
    if index == len(closes) - 13:
      break
    else:
      kVal = calcK(closeChunk)
      kList.append(kVal)
  
  smoothedKList = []
  for index, price in enumerate(kList):
    kChunk = kList[index : index + 3]
    if index == len(kList) - 2:
      break
    else:
      smoothK = calcSMA(kChunk)
      smoothedKList.append(smoothK)
  return smoothedKList

def getBBands(closes):
  BBandDict = {
    'upper': [],
    'mid': [],
    'lower': []
  }
  for index, price in enumerate(closes):
    closeChunk = closes[index : index + 21]
    if index == len(closes) - 20:
      break
    else: 
      sma = calcSMA(closeChunk)
      standardDev = calcStandardDev(closeChunk)
      upper = round(sma + (2 * standardDev), 4)
      lower = round(sma - (2 * standardDev), 4)

      BBandDict['upper'].append(upper)
      BBandDict['mid'].append(sma)
      BBandDict['lower'].append(lower)

  return BBandDict

if __name__ == "__main__":
  main()