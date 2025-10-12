from datetime import datetime
from typing import Dict, List, Any
from .broker_portofolio import BrokerPortofolio


class XtbPortofolio(BrokerPortofolio):
    """
    XTB broker-specific portfolio implementation.
    Supports importing transaction data from CSV files.
    """

    def __init__(self):
        super().__init__()
        self.broker_name = "XTB"
        self.transactions = []

    @staticmethod
    def createFromCsv(csv_reader) -> "XtbPortofolio":
        """
        Create an XtbPortofolio instance from a CSV file reader.

        Args:
            csv_reader: A CSV reader object from the standard csv library

        Returns:
            XtbPortofolio: A new instance populated with data from the CSV

        Raises:
            ValueError: If the CSV format is invalid or required fields are missing
        """
        portfolio = XtbPortofolio()

        # Read the header row
        try:
            header = next(csv_reader)
        except StopIteration:
            raise ValueError("CSV file is empty")

        # Validate header
        expected_headers = ["ID", "Type", "Time", "Comment", "Symbol", "Amount"]
        if header != expected_headers:
            raise ValueError(
                f"Invalid CSV header. Expected {expected_headers}, got {header}"
            )

        # Process each row
        for row_num, row in enumerate(
            csv_reader, start=2
        ):  # Start at 2 because header is row 1
            if len(row) != len(expected_headers):
                raise ValueError(
                    f"Row {row_num}: Expected {len(expected_headers)} columns, got {len(row)}"
                )

            # Validate and parse the row
            transaction = XtbPortofolio._parse_transaction_row(row, row_num)
            portfolio.transactions.append(transaction)

            # Process the transaction based on its type
            XtbPortofolio._process_transaction(portfolio, transaction)

        return portfolio

    @staticmethod
    def _parse_transaction_row(row: List[str], row_num: int) -> Dict[str, Any]:
        """
        Parse and validate a single transaction row from the CSV.

        Args:
            row: List of string values from the CSV row
            row_num: Row number for error reporting

        Returns:
            Dict containing parsed transaction data

        Raises:
            ValueError: If validation fails
        """
        transaction = {}

        # Parse ID (not empty, string)
        transaction["id"] = row[0].strip()
        if not transaction["id"]:
            raise ValueError(f"Row {row_num}: ID cannot be empty")

        # Parse Type (transaction type)
        transaction["type"] = row[1].strip()

        # Parse Time (not empty string with format "%d/%m/%Y %H:%M:%S")
        time_str = row[2].strip()
        if not time_str:
            raise ValueError(f"Row {row_num}: Time cannot be empty")

        try:
            transaction["time"] = datetime.strptime(time_str, "%d/%m/%Y %H:%M:%S")
        except ValueError as e:
            raise ValueError(
                f"Row {row_num}: Invalid time format '{time_str}'. Expected format: 'DD/MM/YYYY HH:MM:SS'"
            ) from e

        # Parse Comment (string)
        transaction["comment"] = row[3].strip()

        # Parse Symbol (string)
        transaction["symbol"] = row[4].strip()

        # Parse Amount (number) - handle European format with comma as decimal separator
        amount_str = row[5].strip()
        try:
            # Replace comma with dot for European number format
            amount_str_normalized = amount_str.replace(",", ".")
            transaction["amount"] = float(amount_str_normalized)
        except ValueError as e:
            raise ValueError(
                f"Row {row_num}: Invalid amount '{amount_str}'. Must be a number"
            ) from e

        return transaction

    @staticmethod
    def _process_transaction(portfolio: "XtbPortofolio", transaction: Dict[str, Any]):
        """
        Process a transaction based on its type and call the appropriate method in BrokerPortofolio.

        Args:
            portfolio: The portfolio instance to update
            transaction: The parsed transaction data
        """
        transaction_type = transaction["type"]
        amount = transaction["amount"]
        timestamp = transaction["time"]
        symbol = transaction["symbol"]
        comment = transaction["comment"]

        if transaction_type == "deposit":
            if amount <= 0:
                raise ValueError(f"Deposit amount must be positive, got {amount}")
            portfolio.add_deposit(amount, timestamp, comment)

        elif transaction_type == "DIVIDENT":
            if amount <= 0:
                raise ValueError(f"Dividend amount must be positive, got {amount}")
            portfolio.add_dividend(amount, timestamp, symbol, comment)

        elif transaction_type == "Free-funds Interest":
            if amount <= 0:
                raise ValueError(
                    f"Free funds interest amount must be positive, got {amount}"
                )
            portfolio.add_free_funds_interest(amount, timestamp, comment)

        elif transaction_type == "Free-funds Interest Tax":
            if amount >= 0:
                raise ValueError(
                    f"Free funds interest tax amount must be negative, got {amount}"
                )
            portfolio.add_free_funds_interest_tax(amount, timestamp, comment)

        elif transaction_type == "Stock purchase":
            if amount >= 0:
                raise ValueError(
                    f"Stock purchase amount must be negative, got {amount}"
                )

            # Parse the comment to extract number of stocks and price
            number_of_stocks, price_per_share = (
                XtbPortofolio._parse_stock_purchase_comment(comment)
            )
            portfolio.add_stock_purchase(
                symbol, amount, timestamp, number_of_stocks, price_per_share, comment
            )

        else:
            # For unknown transaction types, just store the transaction without processing
            pass

    @staticmethod
    def _parse_stock_purchase_comment(comment: str) -> tuple[int, float]:
        """
        Parse the stock purchase comment to extract number of stocks and price per share.

        Expected format: "OPEN BUY $number_of_stocks @ price_per_share"
        Examples:
        - "OPEN BUY 10 @ 30.066"
        - "OPEN BUY 3/35 @ 5.8760" (ignores the "/35" part)

        Args:
            comment: The comment string to parse

        Returns:
            Tuple of (number_of_stocks, price_per_share)

        Raises:
            ValueError: If the comment format is invalid
        """
        import re

        # Pattern to match "OPEN BUY $number @ price" or "OPEN BUY number/ignored @ price"
        # The pattern captures the number before any "/" and ignores everything after "/" until "@"
        pattern = r"OPEN BUY \$?(\d+(?:\.\d+)?)(?:/[^\s@]*)?\s*@\s*(\d+(?:\.\d+)?)"
        match = re.search(pattern, comment)

        if not match:
            raise ValueError(
                f"Invalid stock purchase comment format: '{comment}'. "
                f"Expected format: 'OPEN BUY $number_of_stocks @ price_per_share' or "
                f"'OPEN BUY number/ignored @ price_per_share'"
            )

        try:
            number_of_stocks = int(float(match.group(1)))
            price_per_share = float(match.group(2))

            if number_of_stocks <= 0:
                raise ValueError(
                    f"Number of stocks must be positive, got {number_of_stocks}"
                )

            if price_per_share <= 0:
                raise ValueError(
                    f"Price per share must be positive, got {price_per_share}"
                )

            return number_of_stocks, price_per_share

        except ValueError as e:
            raise ValueError(
                f"Error parsing stock purchase comment '{comment}': {e}"
            ) from e

    def get_transactions(self) -> List[Dict[str, Any]]:
        """Return all transactions in the portfolio."""
        return self.transactions

    def get_transactions_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        """Return all transactions for a specific symbol."""
        return [t for t in self.transactions if t["symbol"] == symbol]

    def get_transactions_by_type(self, transaction_type: str) -> List[Dict[str, Any]]:
        """Return all transactions of a specific type."""
        return [t for t in self.transactions if t["type"] == transaction_type]

    def get_symbol_transactions(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Return all transactions for a specific symbol.

        Args:
            symbol: The symbol to get transactions for

        Returns:
            List of transaction dictionaries
        """
        return [t for t in self.transactions if t["symbol"] == symbol]
