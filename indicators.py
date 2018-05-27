def getSMA(closes):
  _sum = sum(closes)
  n = len(closes)
  SMA = _sum / n
  return SMA

def getMultiplier(n):
  return (float(2) / (n + 1))

# prevEMA = SMA for first calculation of EMA
# EMA gets accurate over time, first calc using SMA way off...
def getEMA(currentPrice, prevEMA, mult):
  EMA = (currentPrice - prevEMA) * mult + prevEMA
  return EMA
  

# avgGain = (totalGainsOverN / N)
# avgLoss = (totalLossesOverN / N)
def getAvgGainLoss(closes):
  avgGainLoss = {
    'gain': 0,
    'loss': 0
  }

  for index, price in enumerate(closes):
    if index == 0:
      pass
    else:
      print(index)
      diff = price - closes[index - 1]
      diff = round(diff, 4)
      if diff > 0:
        avgGainLoss['gain'] += diff
      if diff < 0:
        avgGainLoss['loss'] += abs(diff)

  return avgGainLoss


# # RS
# firstRS = avgGain / avgLoss
# smoothedRS = [((n - 1) * prevAvgGain + currGain) / n] / [((n - 1) * prevAvgLoss + currLoss) / n]
def getRS(avgGainLoss):
  print avgGainLoss
  firstRS = (avgGainLoss['gain'] / avgGainLoss['loss'])
  return firstRS


# # RSI
# 100 - (100 / (1 + RS))
def getRSI(RS):
  return (100 - (100 / (1 + .5702)))