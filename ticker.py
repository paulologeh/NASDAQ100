import sys
import csv
from marketdata import Marketdata
from datetime import datetime
from tqdm import tqdm


def getSymbols(file='nasdaq100stocks.csv'):
    '''
    read in all stocks in the nasdaq100 from a file
    '''
    symbols = []
    with open(file, 'r') as csvfile:
        data = csv.reader(csvfile)
        for symbol in data:
            if symbol[0] == 'Symbol':
                continue
            symbols.append(symbol)
    return symbols


def info():
    '''
    gives information on how to use ticker tool
    '''
    usage = '''NASDAQ 100 ticker tool
    ** Command line tool to look up market data about any stock in the NASDAQ100 **
    Usage
        python3 ticker.py [info]                     usage manual
        python3 ticker.py [list]                     lists all stocks in the NASDAQ 100
        python3 ticker.py [list] [sort]              lists all stocks in the NASDAQ 100 sorted by name
        python3 ticker.py [list] [sort-price]        lists all stocks in the NASDAQ 100 sorted by current price lowest to highest
        python3 ticker.py [search] [term]            looks up the stock in the NASDAQ 100 and returns symbol and name of the listing
        python3 ticker.py [symbol]                   get's all data about the closest matching stock to symbol
        python3 ticker.py [symbol] [price]           gets price of the symbol
        python3 ticker.py [symbol] [todays-high]     gets today's high
        python3 ticker.py [symbol] [52-week-high]    gets 52 week high
        python3 ticker.py [symbol] [previous-close]  gets previous close
        python3 ticker.py [highest]                  returns stock with highest price
        python3 ticker.py [lowest]                   returns stock with lowest price
        python3 ticker.py [winner]                   returns stock with highest percentage gain from the previous close
        python3 ticker.py [looser]                   returns stock with lowest percentage gain from the previous close'''

    print(usage)


def _list(_type=None):
    '''
    lists all symbols of the nasdaq100 in unsorted, sorted by name or sorted by price
    '''
    symbols = getSymbols()  # gets all symbols
    if _type == None:   # unsorted print
        print('Symbol       Name')
        for symbol in symbols:
            print('{} {}'.format(symbol[0].upper(), symbol[1]))
    elif _type == 'sort':   # sorted by name print
        symbols.sort()
        for symbol in symbols:
            print('{} {}'.format(symbol[0].upper(), symbol[1]))
    elif _type == 'sort-price':  # sorted by price print
        mktData = Marketdata()
        symbolsAndPrice = []
        pbar = tqdm(symbols)
        for symbol in pbar:
            pbar.set_description("Fetching data")
            price = mktData.getPrice(symbol[0].upper())
            price = float(price)
            symbol.append(price)
            symbolsAndPrice.append(symbol)

        symbolsAndPrice = sorted(symbolsAndPrice, key=lambda x: x[2])
        print('Symbol   Name    Price($)')
        for symbol in symbolsAndPrice:
            print(symbol[0], symbol[1], symbol[2])


def lookup(term, out=None):
    '''
    looks up market data for the stock in term
    '''
    symbols = getSymbols()
    mktData = Marketdata()
    notFound = term
    term = term.upper()
    for symbol in symbols:
        if term in symbol[0].upper() or term in symbol[1]:
            ticker = symbol[0].upper()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if out == 'price':
                stdout = ''' Ticker: {} ({})
        Price:${} As of {}'''.format(ticker, symbol[1], mktData.getPrice(ticker), current_time)
            elif out == 'todays-high':
                stdout = ''' Ticker: {} ({})
        Todays High:${} As of {}'''.format(ticker, symbol[1], mktData.getDaysHigh(ticker), current_time)
            elif out == '52-week-high':
                stdout = ''' Ticker: {} ({})
        52 week High:${} As of {}'''.format(ticker, symbol[1], mktData.get52WeekHigh(ticker), current_time)
            elif out == 'previous-close':
                stdout = ''' Ticker: {} ({})
        Previous close:${} As of {}'''.format(ticker, symbol[1], mktData.get52WeekHigh(ticker), current_time)
            else:
                stdout = ''' Ticker: {} ({})
                Price:${}   Todays High:${}    52 Week High:${}    Previous Close:${}   As of {}'''.format(
                    ticker,
                    symbol[1],
                    mktData.getPrice(ticker),
                    mktData.getDaysHigh(ticker),
                    mktData.get52WeekHigh(ticker),
                    mktData.getPreviousClose(ticker),
                    current_time
                )
            print(stdout)
            sys.exit()
    print('Could not find {}'.format(notFound))


def search(term):
    '''
    searches for stock in the list of NASDAQ 100 stocks
    '''
    symbols = getSymbols()
    for symbol in symbols:
        if term.upper() in symbol[0].upper() or term.upper() in symbol[1].upper():
            print('{} {}'.format(symbol[0].upper(), symbol[1]))
            return
    print('{} not found'.format(term))


def find(mode):
    '''
    finds the highest, lowest, winning or loosing stock in the nasdaq 100
    '''
    symbols = getSymbols()
    value = {'price': None, 'percent': None, 'previous close': None}
    mktData = Marketdata()
    pbar = tqdm(symbols)
    for symbol in pbar:
        pbar.set_description("Fetching data")
        price = mktData.getPrice(symbol[0].upper())
        price = float(price)
        if mode == 'winner' or mode == 'looser':
            previousClose = float(mktData.getPreviousClose(symbol[0].upper()))
            percent = price / previousClose - 1
        else:
            previousClose = None
            percent = None

        if value['price'] == None:
            value['price'] = price
            value['symbol'] = symbol[0].upper()
            value['name'] = symbol[1]
            value['percent'] = percent
            value['previous close'] = previousClose
        elif mode == 'highest' and price > value['price']:
            value['price'] = price
            value['symbol'] = symbol[0].upper()
            value['name'] = symbol[1]
        elif mode == 'lowest' and price < value['price']:
            value['price'] = price
            value['symbol'] = symbol[0].upper()
            value['name'] = symbol[1]
        elif mode == 'winner' and percent > value['percent']:
            value['price'] = price
            value['symbol'] = symbol[0].upper()
            value['name'] = symbol[1]
            value['percent'] = percent
            value['previous close'] = previousClose
        elif mode == 'looser' and percent < value['percent']:
            value['price'] = price
            value['symbol'] = symbol[0].upper()
            value['name'] = symbol[1]
            value['percent'] = percent
            value['previous close'] = previousClose

    print('{} is {} @ ${}'.format(mode, value['symbol'], value['price']))
    if mode == 'looser' or mode == 'winner':
        print('with a {:.2f}% change from the previous close price of {}'.format(
            100*value['percent'], value['previous close']))


if __name__ == "__main__":

    nArg = len(sys.argv)
    if nArg == 1:
        info()  # print usage info
    elif nArg >= 2:
        arg = sys.argv[1]
        if arg == 'info':
            info()  # print usage info
        elif arg == 'list':
            if nArg == 3:
                _type = sys.argv[2]
                _list(_type)
            else:
                _list()  # list all the stocks in the nasdaq100
        elif arg == 'search':
            term = sys.argv[2]
            search(term)
        else:
            if nArg == 3:
                data = sys.argv[2]
                # Looks up the symbol with specific data point
                lookup(arg, data)
            elif arg == 'highest' or arg == 'lowest' or arg == 'winner' or arg == 'looser':
                find(arg)
            else:
                lookup(arg)  # Look up all available data for the symbol
