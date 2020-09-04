import csv
from marketdata import Marketdata


def getSymbols(file='nasdaq100stocks.csv'):
    '''
    read in stocks from file
    '''
    symbols = []
    with open(file, 'r') as csvfile:
        data = csv.reader(csvfile)
        for symbol in data:
            if symbol[0] == 'Symbol':
                continue
            symbols.append(symbol)
    return symbols


if __name__ == "__main__":
    symbols = getSymbols()
    mktData = Marketdata()
    for symbol in symbols:
        print(symbol[0].upper())
        print(mktData.getPrice(symbol[0].upper()))
        print(mktData.getDaysHigh(symbol[0].upper()))
        print(mktData.get52WeekHigh(symbol[0].upper()))
        print(mktData.getPreviousClose(symbol[0].upper()))
        break
