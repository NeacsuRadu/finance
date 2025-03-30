import yfinance as yf

from investments.date import Date


class Position:

    def __init__(self, ticker: str):
        self.yf_ticker = yf.Ticker(ticker)

    def getPriceOn(self, date: Date):
        if date.isWeekDay():
            return self.__getTickerOpenPriceOn(date)

        return self.__getTickerClosePriceOn(date.getLastWeekDayDate())

    def __getTickerOpenPriceOn(self, date: Date):
        start_date = date
        end_date = date.getNextDay()

        history = self.yf_ticker.history(
            start=start_date.toString(), end=end_date.toString()
        )

        return round(history.loc[start_date.toString(), "Open"], 2)

    def __getTickerClosePriceOn(self, date: Date):
        start_date = date
        end_date = date.getNextDay()

        history = self.yf_ticker.history(
            start=start_date.toString(), end=end_date.toString()
        )

        return round(history.loc[start_date.toString(), "Close"], 2)
