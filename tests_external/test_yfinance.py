import yfinance as yf

import unittest


class TestYFinance(unittest.TestCase):
    def test_getOpenPriceForDay(self):
        ticker = yf.Ticker('EUNL.DE')

        history = ticker.history(start='2025-03-05', end='2025-03-06')

        price = round(history.loc['2025-03-05', 'Open'], 2)

        self.assertEqual(price, 102.40)
    
    def test_getClosePriceForDay(self):
        ticker = yf.Ticker('EUNL.DE')

        history = ticker.history(start='2025-03-25', end='2025-03-26')

        price = round(history.loc['2025-03-25', 'Close'], 2)

        self.assertEqual(price, 100.86)

if __name__ == "__main__":
    unittest.main()
