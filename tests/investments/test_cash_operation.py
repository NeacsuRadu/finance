import unittest
from investments.cash_operation import CashOperation
from datetime import datetime

class TestCashOperation(unittest.TestCase):
    def setUp(self):
        timestamp = round(datetime.strptime("06.08.2024 10:25:39", "%d.%m.%Y %H:%M:%S").timestamp())
        self.op = CashOperation("deposit", 32.5, timestamp)

    def test_getTypeReturnsType(self):
        self.assertEqual(self.op.getType(), "deposit")
    
    def test_getAmountReturnsAmount(self):
        self.assertEqual(self.op.getAmount(), 32.5)
    
    def test_isBeforeReturnsTrueIfParamIsInFuture(self):
        timestamp = round(datetime.strptime("12.09.2024 11:25:39", "%d.%m.%Y %H:%M:%S").timestamp())
        self.assertTrue(self.op.isBefore(timestamp))
    
    def test_isBeforeReturnsFalseIfParamIsInPast(self):
        timestamp = round(datetime.strptime("12.09.2023 11:25:39", "%d.%m.%Y %H:%M:%S").timestamp())
        self.assertFalse(self.op.isBefore(timestamp))

if __name__ == "__main__":
    unittest.main()