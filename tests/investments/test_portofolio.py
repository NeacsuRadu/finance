import unittest
from investments.portofolio import Portofolio


class TestPortofolio(unittest.TestCase):
    def test_depositIncreasesCash(self):
        p = Portofolio()
        p.addDeposit(213)
        self.assertEqual(p.cash, 213)

    def test_depositAddsCashOperation(self):
        p = Portofolio()
        p.addDeposit(213)
        self.assertEqual(len(p.cashOperations), 1)


if __name__ == '__main__':
    unittest.main()
