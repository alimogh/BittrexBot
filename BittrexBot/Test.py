import sys, getopt
from bittrex import Bittrex
from BotAnalysis import BotAnalysis
from bottrade import BotTrade

def main(argv):

    trader = BotTrade("BTC-XMR")


if __name__ == "__main__":
    main(sys.argv[1:])
