import unittest

from investments.position import Position
from investments.ticker.ticker import Ticker
from investments.date import Date


class FakeTicker(Ticker):
    def getPriceOn(self, date: Date):
        test_date = Date(20, 4, 2024)

        if date.isBefore(test_date):
            return 52.3

        return 67.5

    def getTickerName(self) -> str:
        return "FAKE"


class TestPosition(unittest.TestCase):
    def setUp(self):
        ticker = FakeTicker()

        self.position = Position(ticker)
        self.position.registerBuy(Date(12, 3, 2024), 15)
        self.position.registerBuy(Date(17, 4, 2024), 16)
        self.position.registerSell(Date(25, 5, 2024), 13)

    def test_getValueReturnsZeroBeforeBuys(self):
        date = Date(10, 3, 2024)

        self.assertEqual(self.position.getValueOn(date), 0)

    def test_getValueTakesIntoAccountPrice(self):
        date1 = Date(19, 4, 2024)

        self.assertEqual(self.position.getValueOn(date1), 1621.3)

        date2 = Date(21, 4, 2024)

        self.assertEqual(self.position.getValueOn(date2), 2092.5)

    def test_getvalueTakesIntoAccountAmmount(self):
        date = Date(26, 5, 2024)

        self.assertEqual(self.position.getValueOn(date), 1215)


if __name__ == "__main__":
    unittest.main()
