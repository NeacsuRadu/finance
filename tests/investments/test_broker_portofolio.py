import unittest
from datetime import datetime
from investments.portofolio import BrokerPortofolio
from investments.cash_operation import (
    CASH,
    DIVIDEND,
    FREE_FUNDS_INTEREST,
    FREE_FUNDS_INTEREST_TAX,
    STOCK_PURCHASE,
)


class TestBrokerPortofolio(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.portfolio = BrokerPortofolio()

    def test_initialization(self):
        """Test that BrokerPortofolio initializes correctly."""
        self.assertEqual(self.portfolio.broker_name, "Unknown")
        self.assertEqual(self.portfolio.cash, 0)
        self.assertEqual(len(self.portfolio.cashOperations), 0)
        self.assertEqual(len(self.portfolio.positions), 0)

    def test_get_broker_name(self):
        """Test getting broker name."""
        self.assertEqual(self.portfolio.get_broker_name(), "Unknown")

    def test_add_deposit_with_timestamp(self):
        """Test adding deposit with timestamp and comment."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        self.portfolio.add_deposit(500, timestamp, "Test deposit")

        self.assertEqual(self.portfolio.cash, 500)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

        operation = self.portfolio.cashOperations[0]
        self.assertEqual(operation.getType(), CASH)
        self.assertEqual(operation.getAmount(), 500)
        self.assertEqual(operation.timestamp, timestamp)

    def test_add_deposit_negative_amount_raises_error(self):
        """Test that adding negative deposit amount raises ValueError."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_deposit(-100, timestamp)
        self.assertIn("Deposit amount must be positive", str(context.exception))

    def test_add_dividend(self):
        """Test adding dividend payment."""
        timestamp = datetime(2024, 2, 20, 0, 0, 0)
        self.portfolio.add_dividend(25.50, timestamp, "AAPL", "Apple dividend")

        self.assertAlmostEqual(self.portfolio.cash, 25.50, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

        operation = self.portfolio.cashOperations[0]
        self.assertEqual(operation.getType(), DIVIDEND)
        self.assertAlmostEqual(operation.getAmount(), 25.50, places=2)
        self.assertEqual(operation.timestamp, timestamp)

    def test_add_dividend_negative_amount_raises_error(self):
        """Test that adding negative dividend amount raises ValueError."""
        timestamp = datetime(2024, 2, 20, 0, 0, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_dividend(-25.50, timestamp, "AAPL")
        self.assertIn("Dividend amount must be positive", str(context.exception))

    def test_add_free_funds_interest(self):
        """Test adding free funds interest."""
        timestamp = datetime(2024, 3, 1, 0, 0, 0)
        self.portfolio.add_free_funds_interest(2.50, timestamp, "Monthly interest")

        self.assertAlmostEqual(self.portfolio.cash, 2.50, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

        operation = self.portfolio.cashOperations[0]
        self.assertEqual(operation.getType(), FREE_FUNDS_INTEREST)
        self.assertAlmostEqual(operation.getAmount(), 2.50, places=2)
        self.assertEqual(operation.timestamp, timestamp)

    def test_add_free_funds_interest_negative_amount_raises_error(self):
        """Test that adding negative interest amount raises ValueError."""
        timestamp = datetime(2024, 3, 1, 0, 0, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_free_funds_interest(-2.50, timestamp)
        self.assertIn(
            "Free funds interest amount must be positive", str(context.exception)
        )

    def test_add_free_funds_interest_tax(self):
        """Test adding free funds interest tax."""
        timestamp = datetime(2024, 3, 1, 0, 0, 0)
        self.portfolio.add_free_funds_interest_tax(-0.50, timestamp, "Tax on interest")

        self.assertAlmostEqual(self.portfolio.cash, -0.50, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

        operation = self.portfolio.cashOperations[0]
        self.assertEqual(operation.getType(), FREE_FUNDS_INTEREST_TAX)
        self.assertAlmostEqual(operation.getAmount(), -0.50, places=2)
        self.assertEqual(operation.timestamp, timestamp)

    def test_add_free_funds_interest_tax_positive_amount_raises_error(self):
        """Test that adding positive tax amount raises ValueError."""
        timestamp = datetime(2024, 3, 1, 0, 0, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_free_funds_interest_tax(0.50, timestamp)
        self.assertIn(
            "Free funds interest tax amount must be negative", str(context.exception)
        )

    def test_add_stock_purchase(self):
        """Test adding stock purchase."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        self.portfolio.add_stock_purchase(
            "AAPL", -300.66, timestamp, 10, 30.066, "Buy Apple"
        )

        self.assertAlmostEqual(self.portfolio.cash, -300.66, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)
        self.assertEqual(len(self.portfolio.positions), 1)

        # Check cash operation
        operation = self.portfolio.cashOperations[0]
        self.assertEqual(operation.getType(), STOCK_PURCHASE)
        self.assertAlmostEqual(operation.getAmount(), -300.66, places=2)
        self.assertEqual(operation.timestamp, timestamp)

        # Check position
        self.assertIn("AAPL", self.portfolio.positions)
        position = self.portfolio.positions["AAPL"]
        self.assertIsNotNone(position)

    def test_add_stock_purchase_positive_amount_raises_error(self):
        """Test that adding positive stock purchase amount raises ValueError."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_stock_purchase("AAPL", 300.66, timestamp, 10, 30.066)
        self.assertIn("Stock purchase amount must be negative", str(context.exception))

    def test_add_stock_purchase_zero_stocks_raises_error(self):
        """Test that adding zero stocks raises ValueError."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_stock_purchase("AAPL", -300.66, timestamp, 0, 30.066)
        self.assertIn("Number of stocks must be positive", str(context.exception))

    def test_add_stock_purchase_zero_price_raises_error(self):
        """Test that adding zero price per share raises ValueError."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        with self.assertRaises(ValueError) as context:
            self.portfolio.add_stock_purchase("AAPL", -300.66, timestamp, 10, 0)
        self.assertIn("Price per share must be positive", str(context.exception))

    def test_get_positions(self):
        """Test getting all positions."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        self.portfolio.add_stock_purchase("AAPL", -300.66, timestamp, 10, 30.066)
        self.portfolio.add_stock_purchase("MSFT", -200.00, timestamp, 5, 40.00)

        positions = self.portfolio.get_positions()
        self.assertEqual(len(positions), 2)
        self.assertIn("AAPL", positions)
        self.assertIn("MSFT", positions)

    def test_get_position(self):
        """Test getting a specific position."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        self.portfolio.add_stock_purchase("AAPL", -300.66, timestamp, 10, 30.066)

        position = self.portfolio.get_position("AAPL")
        self.assertIsNotNone(position)

        non_existent = self.portfolio.get_position("NONEXISTENT")
        self.assertIsNone(non_existent)

    def test_get_symbols(self):
        """Test getting all symbols."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        self.portfolio.add_stock_purchase("AAPL", -300.66, timestamp, 10, 30.066)
        self.portfolio.add_stock_purchase("MSFT", -200.00, timestamp, 5, 40.00)

        symbols = self.portfolio.get_symbols()
        self.assertEqual(len(symbols), 2)
        self.assertIn("AAPL", symbols)
        self.assertIn("MSFT", symbols)

    def test_get_cash_operations_summary(self):
        """Test getting cash operations summary."""
        timestamp1 = datetime(2024, 1, 1, 0, 0, 0)
        timestamp2 = datetime(2024, 1, 15, 10, 30, 0)

        self.portfolio.add_deposit(1000, timestamp1)
        self.portfolio.add_dividend(25.50, timestamp2, "AAPL")

        summary = self.portfolio.get_cash_operations_summary()

        self.assertAlmostEqual(summary["total_cash"], 1025.50, places=2)
        self.assertEqual(summary["total_operations"], 2)
        self.assertEqual(len(summary["operations_by_type"]), 2)
        self.assertEqual(len(summary["operations"]), 2)

        # Check operations by type
        self.assertIn(CASH, summary["operations_by_type"])
        self.assertIn(DIVIDEND, summary["operations_by_type"])

        self.assertEqual(summary["operations_by_type"][CASH]["count"], 1)
        self.assertEqual(summary["operations_by_type"][CASH]["total_amount"], 1000)
        self.assertEqual(summary["operations_by_type"][DIVIDEND]["count"], 1)
        self.assertAlmostEqual(
            summary["operations_by_type"][DIVIDEND]["total_amount"], 25.50, places=2
        )

    def test_get_portfolio_summary(self):
        """Test getting portfolio summary."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        self.portfolio.add_deposit(1000, timestamp)
        self.portfolio.add_stock_purchase("AAPL", -300.66, timestamp, 10, 30.066)

        summary = self.portfolio.get_portfolio_summary()

        self.assertEqual(summary["broker_name"], "Unknown")
        self.assertAlmostEqual(summary["total_cash"], 699.34, places=2)
        self.assertEqual(summary["positions_count"], 1)
        self.assertEqual(len(summary["symbols"]), 1)
        self.assertIn("AAPL", summary["symbols"])
        self.assertIn("cash_operations_summary", summary)


if __name__ == "__main__":
    unittest.main()
