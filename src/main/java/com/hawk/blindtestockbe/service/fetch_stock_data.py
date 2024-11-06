import yfinance as yf
from datetime import datetime
import sys
import json

def get_historical_stock_prices(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')
    hist = stock.history(start=start, end=end)
    return hist['Close'].to_dict()

if __name__ == "__main__":
    symbol = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    prices = get_historical_stock_prices(symbol, start_date, end_date)
    print(json.dumps(prices))