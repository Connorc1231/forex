def getSMA(closes):
  _sum = sum(closes)
  n = len(closes)
  SMA = round(_sum / n, 4)
  return SMA

def getMultiplier(n):
  return (float(2) / (n + 1))

# prevEMA = SMA for first calculation of EMA
# EMA gets accurate over time, first calc using SMA way off...
def calcEMA(currentPrice, prevEMA, mult):
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
      # price = closes[index]
      diff = price - closes[index - 1]
      diff = round(diff, 4)
      if diff > 0:
        avgGainLoss['gain'] += (diff / 14)
      if diff < 0:
        avgGainLoss['loss'] += abs(diff / 14)
  return avgGainLoss

# RS

def calcFirstRS(avgGainLoss):
  firstRS = (avgGainLoss['gain'] / avgGainLoss['loss'])
  return firstRS


def calcSmoothedRS(currGainLoss, prevAvgGainLoss):
  n = 14
  currGain = currLoss = 0
  if currGainLoss > 0:
    currGain = currGainLoss
  else: 
    currLoss = abs(currGainLoss)

  # print('GAIN: ' + str(prevAvgGainLoss['gain']) + ' * 13 + ' + str(currGain) + '/ 14'  )
  # print('LOSS: ' + str(prevAvgGainLoss['loss']) + ' * 13 + ' + str(currLoss) + '/ 14'  )
  newAvgGain = (prevAvgGainLoss['gain'] * 13 + currGain) / 14 
  newAvgLoss = (prevAvgGainLoss['loss'] * 13 + currLoss) / 14
  print(newAvgGain, newAvgLoss)
  smoothedRS = newAvgGain / newAvgLoss
  return smoothedRS


# # RSI
# 100 - (100 / (1 + RS))
def calcRSI(RS):
  return (100 - (100 / (1 + RS)))