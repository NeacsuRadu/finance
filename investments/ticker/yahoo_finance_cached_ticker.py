from investments.ticker.ticker import Ticker
from investments.repository import Repository
from investments.date import Date
import yfinance as yf
from typing import Optional


class YahooFinanceCachedTicker(Ticker):
    def __init__(self, ticker: str, repository: Repository):
        self.ticker = ticker
        self.repository = repository
        self.yf_ticker = yf.Ticker(ticker)

    def getPriceOn(self, date: Date) -> Optional[float]:
        row = self.repository.find(ticker=self.ticker, date=date.toString())
        if row is not None and "price" in row:
            return row["price"]
        # Otherwise, fall back to Yahoo Finance API
        if date.isWeekDay():
            price = self._get_open_price_on(date)
        else:
            price = self._get_close_price_on(date.getLastWeekDayDate())
        return price

    def _get_open_price_on(self, date: Date) -> Optional[float]:
        start_date = date
        end_date = date.getNextDay()
        history = self.yf_ticker.history(
            start=start_date.toString(), end=end_date.toString()
        )
        if not history.empty:
            return round(history.loc[start_date.toString(), "Open"], 2)
        return None

    def _get_close_price_on(self, date: Date) -> Optional[float]:
        start_date = date
        end_date = date.getNextDay()
        history = self.yf_ticker.history(
            start=start_date.toString(), end=end_date.toString()
        )
        if not history.empty:
            return round(history.loc[start_date.toString(), "Close"], 2)
        return None

    def getTickerName(self) -> str:
        return self.ticker
