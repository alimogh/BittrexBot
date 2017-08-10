#This class code is modified from the python bittrex binding available on github
#https://github.com/ericsomdahl/python-bittrex

import time
import hmac
import hashlib
from urllib import urlencode
from urlparse import urljoin
from Crypto.Cipher import AES
import getpass, ast, json

BASE_URL = 'https://bittrex.com/api/v1.1/%s'

MARKET_SET = {'getopenorders', 'cancel', 'sellmarket', 'selllimit', 'buymarket', 'buylimit'}

ACCOUNT_SET = {'getbalances', 'getbalance', 'getdepositaddress', 'withdraw', 'getorderhistory', 'getorder'}

def encrypt(api_key, api_secret, export=True, export_fn='secrets.json'):
    cipher = AES.new(getpass.getpass('Input encryption password (string will not show)'))
    api_key_n = cipher.encrypt(api_key)
    api_secret_n = cipher.encrypt(api_secret)
    api = {'key': str(api_key_n), 'secret': str(api_secret_n)}
    if export:
        with open(export_fn, 'w') as outfile:
            json.dump(api, outfile)
    return api

class Bittrex(object):
    def __init__(self, api_key, api_secret):
        self.api_key = str(api_key) if api_key is not None else ''
        self.api_secret = str(api_secret) if api_secret is not None else ''
        
    def api_query(self, method, options=None):
        if not options:
            options = {}
        nonce = str(int(time.time() * 1000))
        method_set = 'public'

        if method in MARKET_SET:
            method_set = 'market'
        elif method in ACCOUNT_SET:
            method_set = 'account'

        request_url = (BASE_URL % method_set) + method + '?'

        if method_set != 'public':
            request_url += 'apikey=' + self.api_key + "&nonce=" + nonce + '&'

        request_url += urlencode(options)
        
        return requests.get(
            request_url,
            headers={"apisign": hmac.new(self.api_secret.encode(), request_url.encode(), hashlib.sha512).hexdigest()}
        ).json()

      #returns the historical data in the form of a JSON file
    #period is the number of units to be analyzed
    #valid values for periods are 'oneMin', 'fiveMin', 'thirtyMin', 'hour', 'week', 'day', and 'month'
    #unit is the number of periods to be returned
    def getHistoricalData(self, market, period, unit):
        request_url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=%s&tickInterval=%s' % (market, unit)
        historicalData = requests.get(request_url,
            headers={"apisign": hmac.new(self.api_secret.encode(), request_url.encode(), hashlib.sha512).hexdigest()}
        ).json()

        return historicalData[-period:]

    def getTicker(self, market):
        return self.api_query('getticker', {'market': market})

    def getBalance(self, currency):
        return self.api_query('getbalance', {'currency': currency})
