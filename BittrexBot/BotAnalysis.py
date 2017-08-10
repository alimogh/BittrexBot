#A class for all of the technical analysis to be done

class BotAnalysis(object):
    def __init__(self, market):
        self.market = str(market)

    def EMA(dataPoints, period):
        if len(dataPoints) >= period:
            sum = 0
            for point in dataPoints[-period:]:
                sum += point['Last']
            return (sum / period)



