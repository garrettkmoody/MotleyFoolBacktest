import requests
import re
from bs4 import BeautifulSoup

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
QUERY_SENTENCE = "The Motley Fool top stocks"

# Set to be the beginning of backtest timeframe
START_YEAR = 2016
START_MONTH_INDEX = 0

# Set to be the end of backtest timeframe
END_YEAR = 2020
END_MONTH_INDEX = 0


def fetchArticleTickers():
    currentYear = START_YEAR
    currentMonthIndex = START_MONTH_INDEX

    with open("monthly_tickers.txt", "w") as f:
        while (currentYear != END_YEAR or currentMonthIndex != END_MONTH_INDEX):
            query = f'{QUERY_SENTENCE} {MONTHS[currentMonthIndex]} {currentYear}'
            duckduckgo_search_url = f"https://duckduckgo.com/html/?q={query}"
            response = requests.get(duckduckgo_search_url, headers={'user-agent': 'my-app/0.0.1'})
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.find_all('a', href=True)
            if search_results:
                print(f"Scraping Result for {MONTHS[currentMonthIndex]} - {currentYear}")
                response = requests.get("https://" + search_results[1]
                                        ['href'][2:], headers={'user-agent': 'my-app/0.0.1'})
                soup = BeautifulSoup(response.text, "html.parser")
                redirect_url = soup.find_all('meta')[1]["content"][6:]
                response = requests.get(redirect_url, headers={'user-agent': 'my-app/0.0.1'})
                soup = BeautifulSoup(response.text, "html.parser")
                tickers = soup.find_all('a', {"class": "ticker-symbol"})
                date_pattern = r'\d{4}/\d{2}/\d{2}'
                matches = re.findall(date_pattern, redirect_url)
                if len(matches) == 0:
                    currentMonthIndex += 1
                    if currentMonthIndex == 12:
                        currentYear += 1
                        currentMonthIndex = 0
                    continue
                f.write(matches[0] + ' : ')
                for ticker in tickers:
                    f.write(ticker.text + ' ')
                f.write('\n')
            else:
                print("No results found.")

            currentMonthIndex += 1
            if currentMonthIndex == 12:
                currentYear += 1
                currentMonthIndex = 0


def main():
    fetchArticleTickers()


if __name__ == "__main__":
    main()
