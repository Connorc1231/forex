"""
To execute, run the following command:

python streaming.py [options]

To show heartbeat, replace [options] by -b or --displayHeartBeat
"""

import requests
import json

from optparse import OptionParser
from decimal import *
from config import *


def connect_to_stream():
  """
  Environment                 Description 
  fxTrade (Live)              The live (real money) environment 
  fxTrade Practice (Demo)     The demo (simulated money) environment 
  """
  domainDict = {
    'live': 'stream-fxtrade.oanda.com',
    'demo': 'stream-fxpractice.oanda.com'
    }

  # Set variables
  environment = "demo" # Specify live or demo environment
  instruments = 'EUR_USD' # Desired instrument
  domain = domainDict[environment] 

  try:
    s = requests.Session()
    url = 'https://' + domain + '/v3/accounts/' + account_id + '/pricing/stream'
    headers = {
      'Authorization': 'Bearer ' + access_token,
      # 'X-Accept-Datetime-Format' : 'unix'
    }
    params = {'instruments': instruments}
    req = requests.Request('GET', url, headers = headers, params = params)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    return resp

  except Exception as e:
    s.close()
    print("Caught exception when connecting to stream: " + str(e)) 

def stream(displayHeartbeat):
  response = connect_to_stream()
  if response.status_code != 200:
    print(response.text)
    return
  for line in response.iter_lines(1):
    if line:
      try:
        line = line.decode('utf-8')
        msg = json.loads(line)
      except Exception as e:
        print("Caught exception when converting message into json: " + str(e))
        return

      if "instrument" in msg or "tick" in msg or displayHeartbeat:
        if 'bids' in line:
          line = parse_line(msg)
        print(line)

def parse_line(line):
  output = {
    'time': line['time'],
    'bid': float(line['bids'][0]['price']),
    'ask': float(line['asks'][0]['price'])
  }
  output['spread'] = float(Decimal(line['asks'][0]['price']) - Decimal(line['bids'][0]['price']))
  return output


def main():
  usage = "usage: %prog [options]"
  parser = OptionParser(usage)
  parser.add_option(
    "-b", "--displayHeartBeat", 
    dest = "verbose", 
    action = "store_true", 
    help = "Display HeartBeat in streaming data"
  )
  displayHeartbeat = False
  (options, args) = parser.parse_args()
  if len(args) > 1:
      parser.error("incorrect number of arguments")
  if options.verbose:
      displayHeartbeat = True
  stream(displayHeartbeat)


if __name__ == "__main__":
    main()

