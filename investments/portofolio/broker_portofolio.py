from .portofolio import Portofolio
from investments.cash_operation import (
    CashOperation,
    CASH,
    DIVIDEND,
    FREE_FUNDS_INTEREST,
    FREE_FUNDS_INTEREST_TAX,
    STOCK_PURCHASE,
)
from investments.position import Position
from investments.ticker.yahoo_finance_ticker import YahooFinanceTicker
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict


class BrokerPortofolio(Portofolio):
    """
    Base class for broker-specific portfolio implementations.
    Extends the basic Portfolio functionality with broker-specific features.
    """

    def __init__(self):
        super().__init__()
        self.broker_name = "Unknown"
        self.positions = {}  # Dictionary to store positions by symbol
        self.cash = 0
        self.cashOperations = []

    def get_broker_name(self):
        """Return the name of the broker."""
        return self.broker_name

    def add_deposit(self, amount: float, timestamp: datetime, comment: str = ""):
        """
        Add a deposit to the portfolio.

        Args:
            amount: Positive amount of the deposit
            timestamp: When the deposit occurred
            comment: Optional comment about the deposit
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        cash_operation = CashOperation(CASH, amount, timestamp)
        self.cashOperations.append(cash_operation)
        self.cash += amount

    def add_dividend(
        self, amount: float, timestamp: datetime, symbol: str, comment: str = ""
    ):
        """
        Add a dividend payment to the portfolio.

        Args:
            amount: Positive amount of the dividend
            timestamp: When the dividend was received
            symbol: Symbol of the stock that paid the dividend
            comment: Optional comment about the dividend
        """
        if amount <= 0:
            raise ValueError("Dividend amount must be positive")

        # Add to cash
        cash_operation = CashOperation(DIVIDEND, amount, timestamp)
        self.cashOperations.append(cash_operation)
        self.cash += amount

    def add_free_funds_interest(
        self, amount: float, timestamp: datetime, comment: str = ""
    ):
        """
        Add free funds interest to the portfolio.

        Args:
            amount: Positive amount of the interest
            timestamp: When the interest was credited
            comment: Optional comment about the interest
        """
        if amount <= 0:
            raise ValueError("Free funds interest amount must be positive")

        cash_operation = CashOperation(FREE_FUNDS_INTEREST, amount, timestamp)
        self.cashOperations.append(cash_operation)
        self.cash += amount

    def add_free_funds_interest_tax(
        self, amount: float, timestamp: datetime, comment: str = ""
    ):
        """
        Add free funds interest tax deduction to the portfolio.

        Args:
            amount: Negative amount of the tax (will be made positive internally)
            timestamp: When the tax was deducted
            comment: Optional comment about the tax
        """
        if amount >= 0:
            raise ValueError("Free funds interest tax amount must be negative")

        # Convert to positive for internal storage
        tax_amount = abs(amount)
        cash_operation = CashOperation(FREE_FUNDS_INTEREST_TAX, -tax_amount, timestamp)
        self.cashOperations.append(cash_operation)
        self.cash -= tax_amount

    def add_stock_purchase(
        self,
        symbol: str,
        amount: float,
        timestamp: datetime,
        number_of_stocks: int,
        price_per_share: float,
        comment: str = "",
    ):
        """
        Add a stock purchase to the portfolio.

        Args:
            symbol: Symbol of the stock being purchased
            amount: Negative amount paid for the purchase (will be made positive internally)
            timestamp: When the purchase occurred
            number_of_stocks: Number of shares purchased
            price_per_share: Price per share
            comment: Optional comment about the purchase
        """
        if amount >= 0:
            raise ValueError("Stock purchase amount must be negative (money going out)")

        if number_of_stocks <= 0:
            raise ValueError("Number of stocks must be positive")

        if price_per_share <= 0:
            raise ValueError("Price per share must be positive")

        # Convert amount to positive for internal storage
        purchase_amount = abs(amount)

        # Deduct from cash
        cash_operation = CashOperation(STOCK_PURCHASE, -purchase_amount, timestamp)
        self.cashOperations.append(cash_operation)
        self.cash -= purchase_amount

        # Add or update position
        if symbol not in self.positions:
            # Create a Yahoo Finance ticker for the position
            ticker = YahooFinanceTicker(symbol)
            self.positions[symbol] = Position(ticker)

        # Register the buy in the position
        from investments.date import Date

        date = Date(timestamp.day, timestamp.month, timestamp.year)
        self.positions[symbol].registerBuy(date, number_of_stocks)

    def get_positions(self) -> Dict[str, Position]:
        """Return all positions in the portfolio."""
        return self.positions

    def get_position(self, symbol: str) -> Position:
        """Get a specific position by symbol."""
        return self.positions.get(symbol)

    def get_cash_operations_summary(self) -> Dict[str, Any]:
        """
        Return a summary of all cash operations.

        Returns:
            Dict containing cash operations summary
        """
        summary = {
            "total_cash": self.cash,
            "total_operations": len(self.cashOperations),
            "operations_by_type": {},
            "operations": [],
        }

        # Count operations by type
        for op in self.cashOperations:
            op_type = op.getType()
            if op_type not in summary["operations_by_type"]:
                summary["operations_by_type"][op_type] = {"count": 0, "total_amount": 0}
            summary["operations_by_type"][op_type]["count"] += 1
            summary["operations_by_type"][op_type]["total_amount"] += op.getAmount()

            # Add operation details
            summary["operations"].append(
                {"type": op_type, "amount": op.getAmount(), "timestamp": op.timestamp}
            )

        return summary

    def get_symbols(self) -> List[str]:
        """
        Return a list of all symbols in the portfolio.

        Returns:
            List of symbol strings
        """
        return list(self.positions.keys())

    def get_symbol_transactions(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Return all transactions for a specific symbol.

        Args:
            symbol: The symbol to get transactions for

        Returns:
            List of transaction dictionaries
        """
        # This method will be overridden in XtbPortofolio to provide actual transaction data
        return []

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """
        Return a comprehensive summary of the portfolio.

        Returns:
            Dict containing portfolio summary
        """
        return {
            "broker_name": self.get_broker_name(),
            "total_cash": self.cash,
            "symbols": self.get_symbols(),
            "positions_count": len(self.positions),
            "cash_operations_summary": self.get_cash_operations_summary(),
        }

    def get_statistics_by_year(self) -> Dict[str, Dict[int, float]]:
        """
        Get portfolio statistics grouped by year.

        Returns:
            Dictionary containing statistics by year
        """
        deposits_by_year = defaultdict(float)
        dividends_by_year = defaultdict(float)
        stock_purchases_by_year = defaultdict(float)

        for operation in self.cashOperations:
            year = operation.timestamp.year
            operation_type = operation.getType()
            amount = operation.getAmount()

            if operation_type == CASH:
                deposits_by_year[year] += amount
            elif operation_type == DIVIDEND:
                dividends_by_year[year] += amount
            elif operation_type == STOCK_PURCHASE:
                # Stock purchases are negative amounts, so we take absolute value
                stock_purchases_by_year[year] += abs(amount)

        return {
            "deposits": dict(deposits_by_year),
            "dividends": dict(dividends_by_year),
            "stock_purchases": dict(stock_purchases_by_year),
        }

    def get_statistics_by_month(self) -> Dict[str, Dict[str, float]]:
        """
        Get portfolio statistics grouped by month.

        Returns:
            Dictionary containing statistics by month
        """
        deposits_by_month = defaultdict(float)
        dividends_by_month = defaultdict(float)
        stock_purchases_by_month = defaultdict(float)

        for operation in self.cashOperations:
            month_key = operation.timestamp.strftime("%Y-%m")
            operation_type = operation.getType()
            amount = operation.getAmount()

            if operation_type == CASH:
                deposits_by_month[month_key] += amount
            elif operation_type == DIVIDEND:
                dividends_by_month[month_key] += amount
            elif operation_type == STOCK_PURCHASE:
                # Stock purchases are negative amounts, so we take absolute value
                stock_purchases_by_month[month_key] += abs(amount)

        return {
            "deposits": dict(deposits_by_month),
            "dividends": dict(dividends_by_month),
            "stock_purchases": dict(stock_purchases_by_month),
        }

    def output_statistics(self, statistics: Dict[str, Any]) -> None:
        """
        Output statistics to console.
        This is a basic console implementation. Can be overridden for other output formats.

        Args:
            statistics: Dictionary containing the statistics to output
        """
        print("=" * 60)
        print("PORTFOLIO STATISTICS")
        print("=" * 60)

        # Output deposits
        if "deposits" in statistics:
            print("\nDEPOSITS:")
            print("-" * 20)
            for time_period, amount in sorted(statistics["deposits"].items()):
                print(f"{time_period}: €{amount:,.2f}")

        # Output dividends
        if "dividends" in statistics:
            print("\nDIVIDENDS:")
            print("-" * 20)
            for time_period, amount in sorted(statistics["dividends"].items()):
                print(f"{time_period}: €{amount:,.2f}")

        # Output stock purchases
        if "stock_purchases" in statistics:
            print("\nSTOCK PURCHASES:")
            print("-" * 20)
            for time_period, amount in sorted(statistics["stock_purchases"].items()):
                print(f"{time_period}: €{amount:,.2f}")

        print("=" * 60)
