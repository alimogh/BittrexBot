from bittrex import Bittrex
from BotAnalysis import BotAnalysis

#this is the class that takes care of trading

class BotTrade(object):
    def __init__(self, market, amount, stopLoss=0):
        self.market = market
        self.amount = amount
        self.analyzer = BotAnalysis(self.market)
        self.bittrex = Bittrex('', '')
        if stopLoss:
            self.stopLoss = stopLoss
        self.tradePlaced = False
        self.data = []
        self.prices = []
        self.typeOfTrade = False


    def simpleEMAtrade(self, period, unit):
        ticker = self.bittrex.getTicker(self.market)
        lastPrice = self.ticker['result']['Last']
        self.prices.append(lastPrice)
        self.currentMovingAverage = analyzer.EMA(prices, period)
        self.wallet = self.bittrex.getBalance("BTC")
        self.wallet = float(self.wallet['result']['Available'])

        if len(prices) > 1:
            if not self.tradePlaced:
                if lastPrice > currentMovingAverage and lastPrice < prices[-2]:
                    print "SELL ORDER"
                    self.tradePlaced = True
                    self.typeOfTrade = "short"
                elif lastPrice < currentMovingAverage and lastPrice > previousPrice:
                    print "BUY ORDER"
                    self.tradePlaced = True
                    self.typeOfTrade = 'long'
            elif self.typeOfTrade == 'short':
                if lastPrice < currentMovingAverage:
                    print "EXIT TRADE"
                    self.tradePlaced = False
                    self.typeOfTrade = False
            elif self.typeOfTrade == 'long':
                if lastPrice > currentMovingAverage:
                    print "EXIT TRADE"
                    self.tradePlaced = False

            
