# # RSI
# 100 - (100 / (1 + RS))

# # RS
# firstAvgGain / firstAvgLoss = sumOfGainsOverN / sumOfLossesOverN

# avgGain = prevAvgGain * 13 + currGain

# avgLoss = prevAvgLoss * 13 + currLoss


def getSMA(closes):
  _sum = 0
  n = len(closes)
  for price in closes:
    _sum = _sum + closes[price]
  SMA = _sum / n
  return SMA

def getMultiplier(n):
  return 2 / (n + 1)


def getRSI(OHLCV):
  pass