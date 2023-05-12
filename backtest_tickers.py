from datetime import datetime, timedelta
import yfinance as yf
from statistics import mean

DAYS_HOLDING = 60

def getFutureDates(date_string, days_added):
    date_object = datetime.strptime(date_string, '%Y/%m/%d').date()
    future_date = date_object + timedelta(days=days_added)
    future_date2 = date_object + timedelta(days=days_added + 5)
    return (future_date.strftime('%Y-%m-%d'), future_date2.strftime('%Y-%m-%d'))


def backtest():

    with open("monthly_tickers.txt") as f:
        lines = f.readlines()

        with open("results.txt", "w") as fout:
            totalReturn = 0
            for line in lines:
                line = line.split(' : ')
                currentDates = getFutureDates(line[0], 1)
                futureDates = getFutureDates(line[0], DAYS_HOLDING)
                tickers = line[1].strip().split()
                fout.write(line[0] + ' - Monthly Return : %')
                tickerReturns = []
                for ticker in tickers:
                    print(f"TICKER : {ticker}")
                    stock = yf.download(ticker, interval='1d', start=currentDates[0], end=currentDates[1])
                    if len(stock['Close']) > 0:
                        purchasePrice = stock['Close'][0]
                    else:
                        print("No stock information.")
                    stock = yf.download(ticker, interval='1d', start=futureDates[0], end=futureDates[1])
                    if len(stock['Close']) > 0:
                        salePrice = stock['Close'][0]
                    else:
                        print("No stock information.")

                    tickerReturns.append((salePrice / purchasePrice) - 1)
                fout.write(str(mean(tickerReturns)) + '\n')
                totalReturn += mean(tickerReturns)
            
            fout.write(f"TOTAL RETURN : %{totalReturn}")
                    

def main():
    backtest()
    pass


if __name__ == "__main__":
    main()