import unittest
import csv
import io
from datetime import datetime
from investments.portofolio import XtbPortofolio


class TestXtbPortofolio(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.portfolio = XtbPortofolio()

    def test_initialization(self):
        """Test that XtbPortofolio initializes correctly."""
        self.assertEqual(self.portfolio.broker_name, "XTB")
        self.assertEqual(self.portfolio.cash, 0)
        self.assertEqual(len(self.portfolio.cashOperations), 0)
        self.assertEqual(len(self.portfolio.positions), 0)
        self.assertEqual(len(self.portfolio.transactions), 0)

    def test_createFromCsv_basic_functionality(self):
        """Test creating XtbPortofolio from CSV with basic data."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
1,deposit,01/01/2024 00:00:00,Initial deposit,CASH,1000.00
2,Stock purchase,15/01/2024 10:30:00,OPEN BUY 10 @ 30.066,AAPL,-300.66"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        portfolio = XtbPortofolio.createFromCsv(csv_reader)

        self.assertEqual(portfolio.broker_name, "XTB")
        self.assertEqual(len(portfolio.transactions), 2)
        self.assertAlmostEqual(portfolio.cash, 699.34, places=2)  # 1000 - 300.66
        self.assertEqual(len(portfolio.positions), 1)
        self.assertIn("AAPL", portfolio.positions)

    def test_createFromCsv_european_number_format(self):
        """Test creating XtbPortofolio from CSV with European number format."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
1,deposit,01/01/2024 00:00:00,Initial deposit,CASH,"1000,50"
2,Stock purchase,15/01/2024 10:30:00,"OPEN BUY 5 @ 30,066",AAPL,"-150,33" """

        csv_reader = csv.reader(io.StringIO(csv_data))
        portfolio = XtbPortofolio.createFromCsv(csv_reader)

        self.assertAlmostEqual(portfolio.cash, 850.17, places=2)  # 1000.50 - 150.33
        self.assertEqual(len(portfolio.transactions), 2)

    def test_createFromCsv_invalid_header_raises_error(self):
        """Test that invalid CSV header raises ValueError."""
        csv_data = """Wrong,Header,Format
1,deposit,01/01/2024 00:00:00"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        with self.assertRaises(ValueError) as context:
            XtbPortofolio.createFromCsv(csv_reader)
        self.assertIn("Invalid CSV header", str(context.exception))

    def test_createFromCsv_empty_file_raises_error(self):
        """Test that empty CSV file raises ValueError."""
        csv_data = ""

        csv_reader = csv.reader(io.StringIO(csv_data))
        with self.assertRaises(ValueError) as context:
            XtbPortofolio.createFromCsv(csv_reader)
        self.assertIn("CSV file is empty", str(context.exception))

    def test_createFromCsv_wrong_column_count_raises_error(self):
        """Test that wrong number of columns raises ValueError."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
1,deposit,01/01/2024 00:00:00,Initial deposit,1000.00"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        with self.assertRaises(ValueError) as context:
            XtbPortofolio.createFromCsv(csv_reader)
        self.assertIn("Expected 6 columns, got 5", str(context.exception))

    def test_createFromCsv_invalid_time_format_raises_error(self):
        """Test that invalid time format raises ValueError."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
1,deposit,2024-01-01 00:00:00,Initial deposit,CASH,1000.00"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        with self.assertRaises(ValueError) as context:
            XtbPortofolio.createFromCsv(csv_reader)
        self.assertIn("Invalid time format", str(context.exception))

    def test_createFromCsv_invalid_amount_raises_error(self):
        """Test that invalid amount format raises ValueError."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
1,deposit,01/01/2024 00:00:00,Initial deposit,CASH,invalid_amount"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        with self.assertRaises(ValueError) as context:
            XtbPortofolio.createFromCsv(csv_reader)
        self.assertIn("Invalid amount", str(context.exception))

    def test_createFromCsv_empty_id_raises_error(self):
        """Test that empty ID raises ValueError."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
,deposit,01/01/2024 00:00:00,Initial deposit,CASH,1000.00"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        with self.assertRaises(ValueError) as context:
            XtbPortofolio.createFromCsv(csv_reader)
        self.assertIn("ID cannot be empty", str(context.exception))

    def test_parse_stock_purchase_comment_standard_format(self):
        """Test parsing stock purchase comment in standard format."""
        comment = "OPEN BUY 10 @ 30.066"
        number_of_stocks, price_per_share = XtbPortofolio._parse_stock_purchase_comment(
            comment
        )

        self.assertEqual(number_of_stocks, 10)
        self.assertAlmostEqual(price_per_share, 30.066, places=3)

    def test_parse_stock_purchase_comment_with_dollar_sign(self):
        """Test parsing stock purchase comment with dollar sign."""
        comment = "OPEN BUY $5 @ 25.50"
        number_of_stocks, price_per_share = XtbPortofolio._parse_stock_purchase_comment(
            comment
        )

        self.assertEqual(number_of_stocks, 5)
        self.assertAlmostEqual(price_per_share, 25.50, places=2)

    def test_parse_stock_purchase_comment_with_fraction_format(self):
        """Test parsing stock purchase comment with fraction format."""
        comment = "OPEN BUY 3/35 @ 5.8760"
        number_of_stocks, price_per_share = XtbPortofolio._parse_stock_purchase_comment(
            comment
        )

        self.assertEqual(number_of_stocks, 3)
        self.assertAlmostEqual(price_per_share, 5.8760, places=4)

    def test_parse_stock_purchase_comment_invalid_format_raises_error(self):
        """Test that invalid comment format raises ValueError."""
        comment = "INVALID FORMAT"
        with self.assertRaises(ValueError) as context:
            XtbPortofolio._parse_stock_purchase_comment(comment)
        self.assertIn("Invalid stock purchase comment format", str(context.exception))

    def test_process_transaction_deposit(self):
        """Test processing deposit transaction."""
        transaction = {
            "type": "deposit",
            "amount": 1000.0,
            "time": datetime(2024, 1, 1, 0, 0, 0),
            "symbol": "CASH",
            "comment": "Initial deposit",
        }

        XtbPortofolio._process_transaction(self.portfolio, transaction)

        self.assertAlmostEqual(self.portfolio.cash, 1000.0, places=1)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

    def test_process_transaction_deposit_negative_amount_raises_error(self):
        """Test that negative deposit amount raises ValueError."""
        transaction = {
            "type": "deposit",
            "amount": -1000.0,
            "time": datetime(2024, 1, 1, 0, 0, 0),
            "symbol": "CASH",
            "comment": "Invalid deposit",
        }

        with self.assertRaises(ValueError) as context:
            XtbPortofolio._process_transaction(self.portfolio, transaction)
        self.assertIn("Deposit amount must be positive", str(context.exception))

    def test_process_transaction_dividend(self):
        """Test processing dividend transaction."""
        transaction = {
            "type": "DIVIDENT",
            "amount": 25.50,
            "time": datetime(2024, 2, 20, 0, 0, 0),
            "symbol": "AAPL",
            "comment": "Apple dividend",
        }

        XtbPortofolio._process_transaction(self.portfolio, transaction)

        self.assertAlmostEqual(self.portfolio.cash, 25.50, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

    def test_process_transaction_free_funds_interest(self):
        """Test processing free funds interest transaction."""
        transaction = {
            "type": "Free-funds Interest",
            "amount": 2.50,
            "time": datetime(2024, 3, 1, 0, 0, 0),
            "symbol": "CASH",
            "comment": "Monthly interest",
        }

        XtbPortofolio._process_transaction(self.portfolio, transaction)

        self.assertAlmostEqual(self.portfolio.cash, 2.50, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

    def test_process_transaction_free_funds_interest_tax(self):
        """Test processing free funds interest tax transaction."""
        transaction = {
            "type": "Free-funds Interest Tax",
            "amount": -0.50,
            "time": datetime(2024, 3, 1, 0, 0, 0),
            "symbol": "CASH",
            "comment": "Tax on interest",
        }

        XtbPortofolio._process_transaction(self.portfolio, transaction)

        self.assertAlmostEqual(self.portfolio.cash, -0.50, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)

    def test_process_transaction_stock_purchase(self):
        """Test processing stock purchase transaction."""
        transaction = {
            "type": "Stock purchase",
            "amount": -300.66,
            "time": datetime(2024, 1, 15, 10, 30, 0),
            "symbol": "AAPL",
            "comment": "OPEN BUY 10 @ 30.066",
        }

        XtbPortofolio._process_transaction(self.portfolio, transaction)

        self.assertAlmostEqual(self.portfolio.cash, -300.66, places=2)
        self.assertEqual(len(self.portfolio.cashOperations), 1)
        self.assertEqual(len(self.portfolio.positions), 1)
        self.assertIn("AAPL", self.portfolio.positions)

    def test_process_transaction_stock_purchase_positive_amount_raises_error(self):
        """Test that positive stock purchase amount raises ValueError."""
        transaction = {
            "type": "Stock purchase",
            "amount": 300.66,
            "time": datetime(2024, 1, 15, 10, 30, 0),
            "symbol": "AAPL",
            "comment": "OPEN BUY 10 @ 30.066",
        }

        with self.assertRaises(ValueError) as context:
            XtbPortofolio._process_transaction(self.portfolio, transaction)
        self.assertIn("Stock purchase amount must be negative", str(context.exception))

    def test_get_transactions(self):
        """Test getting all transactions."""
        # Add some transactions manually
        self.portfolio.transactions = [
            {"id": "1", "type": "deposit", "amount": 1000.0},
            {"id": "2", "type": "Stock purchase", "amount": -300.66},
        ]

        transactions = self.portfolio.get_transactions()
        self.assertEqual(len(transactions), 2)

    def test_get_transactions_by_symbol(self):
        """Test getting transactions by symbol."""
        # Add some transactions manually
        self.portfolio.transactions = [
            {"id": "1", "type": "deposit", "symbol": "CASH", "amount": 1000.0},
            {"id": "2", "type": "Stock purchase", "symbol": "AAPL", "amount": -300.66},
            {"id": "3", "type": "Stock purchase", "symbol": "AAPL", "amount": -200.0},
        ]

        aapl_transactions = self.portfolio.get_transactions_by_symbol("AAPL")
        self.assertEqual(len(aapl_transactions), 2)

        cash_transactions = self.portfolio.get_transactions_by_symbol("CASH")
        self.assertEqual(len(cash_transactions), 1)

    def test_get_transactions_by_type(self):
        """Test getting transactions by type."""
        # Add some transactions manually
        self.portfolio.transactions = [
            {"id": "1", "type": "deposit", "amount": 1000.0},
            {"id": "2", "type": "Stock purchase", "amount": -300.66},
            {"id": "3", "type": "Stock purchase", "amount": -200.0},
        ]

        stock_purchases = self.portfolio.get_transactions_by_type("Stock purchase")
        self.assertEqual(len(stock_purchases), 2)

        deposits = self.portfolio.get_transactions_by_type("deposit")
        self.assertEqual(len(deposits), 1)

    def test_get_symbol_transactions(self):
        """Test getting symbol transactions (overridden method)."""
        # Add some transactions manually
        self.portfolio.transactions = [
            {"id": "1", "type": "deposit", "symbol": "CASH", "amount": 1000.0},
            {"id": "2", "type": "Stock purchase", "symbol": "AAPL", "amount": -300.66},
            {"id": "3", "type": "Stock purchase", "symbol": "AAPL", "amount": -200.0},
        ]

        aapl_transactions = self.portfolio.get_symbol_transactions("AAPL")
        self.assertEqual(len(aapl_transactions), 2)

        # Should be the same as get_transactions_by_symbol
        aapl_transactions_alt = self.portfolio.get_transactions_by_symbol("AAPL")
        self.assertEqual(len(aapl_transactions), len(aapl_transactions_alt))

    def test_comprehensive_csv_processing(self):
        """Test comprehensive CSV processing with all transaction types."""
        csv_data = """ID,Type,Time,Comment,Symbol,Amount
1,deposit,01/01/2024 00:00:00,Initial deposit,CASH,1000.00
2,Stock purchase,15/01/2024 10:30:00,OPEN BUY 10 @ 30.066,AAPL,-300.66
3,DIVIDENT,20/02/2024 00:00:00,Apple dividend,AAPL,25.50
4,Free-funds Interest,01/03/2024 00:00:00,Monthly interest,CASH,2.50
5,Free-funds Interest Tax,01/03/2024 00:00:00,Tax on interest,CASH,-0.50
6,Stock purchase,10/03/2024 14:15:00,OPEN BUY 3/35 @ 5.8760,MSFT,-17.63"""

        csv_reader = csv.reader(io.StringIO(csv_data))
        portfolio = XtbPortofolio.createFromCsv(csv_reader)

        # Check final cash balance
        expected_cash = 1000.00 - 300.66 + 25.50 + 2.50 - 0.50 - 17.63
        self.assertAlmostEqual(portfolio.cash, expected_cash, places=2)

        # Check positions
        self.assertEqual(len(portfolio.positions), 2)
        self.assertIn("AAPL", portfolio.positions)
        self.assertIn("MSFT", portfolio.positions)

        # Check transactions
        self.assertEqual(len(portfolio.transactions), 6)

        # Check cash operations
        self.assertEqual(len(portfolio.cashOperations), 6)


if __name__ == "__main__":
    unittest.main()
