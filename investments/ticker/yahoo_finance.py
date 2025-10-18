import yfinance as yf
from investments.repository import Repository
from investments.ticker.ticker import Ticker
from investments.date import Date
from typing import List


class YahooFinance:
    def __init__(self, repository: Repository):
        self.repository = repository

    def download(self, tickers: List[Ticker], start: Date, end: Date):
        ticker_symbols = [t.getTickerName() for t in tickers]
        # Remove possible None in case of wrong object
        ticker_symbols = [s for s in ticker_symbols if s]
        if not ticker_symbols:
            return

        data = yf.download(
            ticker_symbols,
            start=start.toString(),
            end=end.toString(),
            group_by="ticker",
        )

        to_create = []
        # Save to repository: expected columns ['ticker', 'date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        if len(ticker_symbols) == 1:
            ticker = ticker_symbols[0]
            for date, row in data.iterrows():
                row_dict = row.to_dict()
                row_dict.update({"ticker": ticker, "date": date.strftime("%Y-%m-%d")})
                to_create.append(row_dict)
        else:
            for ticker in ticker_symbols:
                sub_df = data[ticker]
                for date, row in sub_df.iterrows():
                    row_dict = row.to_dict()
                    row_dict.update(
                        {"ticker": ticker, "date": date.strftime("%Y-%m-%d")}
                    )
                    to_create.append(row_dict)
        self.repository.create(to_create)
