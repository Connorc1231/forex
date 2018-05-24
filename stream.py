import requests
import json

from config import *
from optparse import OptionParser

def main():



def connect_to_stream():
  domainDict = {
    'demo': 'https://stream-fxpractice.oanda.com/',
    'live': 'https://stream-fxlive.oanda.com/'
  }

  environment = 'demo' # demo or live
  domain = domainDict[environment]
  instrument = 'EUR_USD'

  try:
    s = requests.Session()
    url = 'https://' + domain + '/v3/instruments/' + instrument + '/candles'
    headers = 