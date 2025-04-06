from investments.ticker.ticker import Ticker
from investments.date import Date


class Position:

    def __init__(self, ticker: Ticker):
        self._ticker = ticker
        self._changes = PositionChanges()

    def registerBuy(self, date: Date, amount: float):
        self._changes.registerBuy(date, amount)

    def registerSell(self, date: Date, amount: float):
        self._changes.registerSell(date, amount)

    def getValueOn(self, date: Date):
        amount = self._changes.getAmountOn(date)
        price = self._ticker.getPriceOn(date)

        return amount * price


class PositionChanges:

    def __init__(self):
        self._changes = []

    def registerBuy(self, date: Date, amount: float):
        self._changes.append({"date": date, "amount": amount})

    def registerSell(self, date: Date, amount: float):
        self._changes.append({"date": date, "amount": (-1) * amount})

    def getAmountOn(self, date: Date):
        amount = 0

        for change in self._changes:
            if change["date"].isBefore(date):
                amount += change["amount"]

        return amount
