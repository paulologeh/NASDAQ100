import time
import sys
import requests
from bs4 import BeautifulSoup


class Marketdata:
    '''
    Class to scrape ticker data from yahoo finance
    '''

    def __init__(self):
        pass

    def scrapeYahoo(self, symbol, classValue, reactid, classType='span'):
        url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch'
        response = requests.get(url, timeout=5)

        soup = BeautifulSoup(response.text, 'html.parser')
        Object = soup.find(classType, attrs={
                           'class': classValue, 'data-reactid': reactid})
        time.sleep(0.5)  # to prevent being blocked by yahoo
        if Object == None:
            sys.exit('Error! Failed To fetch market data. Please try again')

        text = Object.text
        text = text.replace(',', '')
        if '-' in text:
            idx = text.index('-')
            text = text[idx+1:]
            text = text.replace(" ", "")
        digit = float(text)
        return text

    def getPrice(self, Symbol):
        # <span class = "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid = "49" > 2,713.60 </span>
        return self.scrapeYahoo(Symbol, "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)", "49")

    def getDaysHigh(self, Symbol):
        # <td class = "Ta(end) Fw(600) Lh(14px)" data-test = "DAYS_RANGE-value" data-reactid = "114" > 75.68 - 79.74 < /td >
        return self.scrapeYahoo(Symbol, "Ta(end) Fw(600) Lh(14px)", "114", 'td')

    def get52WeekHigh(self, Symbol):
        # <td class = "Ta(end) Fw(600) Lh(14px)" data-test = "FIFTY_TWO_WK_RANGE-value" data-reactid = "121" > 1, 626.03 - 3, 552.25 < /td >
        return self.scrapeYahoo(Symbol, "Ta(end) Fw(600) Lh(14px)", "118", 'td')

    def getPreviousClose(self, Symbol):
        # <<span class="Trsdu(0.3s) " data-reactid="97">2,708.98</span>
        return self.scrapeYahoo(Symbol, "Trsdu(0.3s)", "97")
