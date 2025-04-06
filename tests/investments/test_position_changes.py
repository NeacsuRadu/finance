import unittest

from investments.position import PositionChanges
from investments.date import Date


class TestPositionChanges(unittest.TestCase):
    def setUp(self):
        self.changes = PositionChanges()
        self.changes.registerBuy(Date(12, 3, 2024), 15)
        self.changes.registerBuy(Date(17, 4, 2024), 16)
        self.changes.registerSell(Date(25, 5, 2024), 13)

    def test_getAmountReturnsZeroWhenNoChanges(self):
        changes = PositionChanges()
        date = Date(23, 3, 2023)

        self.assertEqual(changes.getAmountOn(date), 0)

    def test_getAmountReturnsZeroBeforeAnyChanges(self):
        date = Date(10, 2, 2024)

        self.assertEqual(self.changes.getAmountOn(date), 0)

    def test_getAmountReturnsSumOfBuys(self):
        date = Date(19, 4, 2024)

        self.assertEqual(self.changes.getAmountOn(date), 31)

    def test_getAmountReturnsSumOfBuysAndSubtractsSells(self):
        date = Date(26, 5, 2024)

        self.assertEqual(self.changes.getAmountOn(date), 18)


if __name__ == "__main__":
    unittest.main()
