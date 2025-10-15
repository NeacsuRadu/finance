from abc import ABC, abstractmethod
from typing import Dict, Any
from collections import defaultdict


class Statistics(ABC):
    """
    Abstract base class for generating portfolio statistics.
    Provides methods for calculating time-based statistics and abstract output methods.
    """

    def __init__(self, portfolio):
        """
        Initialize statistics with a portfolio.

        Args:
            portfolio: The portfolio to generate statistics for
        """
        self.portfolio = portfolio

    def get_deposits_by_year(self) -> Dict[int, float]:
        """
        Calculate total deposits by year.

        Returns:
            Dictionary with year as key and total deposit amount as value
        """
        deposits_by_year = defaultdict(float)

        for operation in self.portfolio.cashOperations:
            if operation.getType() == "deposit":
                year = operation.timestamp.year
                deposits_by_year[year] += operation.getAmount()

        return dict(deposits_by_year)

    def get_deposits_by_month(self) -> Dict[str, float]:
        """
        Calculate total deposits by month (YYYY-MM format).

        Returns:
            Dictionary with month as key (YYYY-MM) and total deposit amount as value
        """
        deposits_by_month = defaultdict(float)

        for operation in self.portfolio.cashOperations:
            if operation.getType() == "deposit":
                month_key = operation.timestamp.strftime("%Y-%m")
                deposits_by_month[month_key] += operation.getAmount()

        return dict(deposits_by_month)

    def get_dividends_by_year(self) -> Dict[int, float]:
        """
        Calculate total dividends by year.

        Returns:
            Dictionary with year as key and total dividend amount as value
        """
        dividends_by_year = defaultdict(float)

        for operation in self.portfolio.cashOperations:
            if operation.getType() == "dividend":
                year = operation.timestamp.year
                dividends_by_year[year] += operation.getAmount()

        return dict(dividends_by_year)

    def get_dividends_by_month(self) -> Dict[str, float]:
        """
        Calculate total dividends by month (YYYY-MM format).

        Returns:
            Dictionary with month as key (YYYY-MM) and total dividend amount as value
        """
        dividends_by_month = defaultdict(float)

        for operation in self.portfolio.cashOperations:
            if operation.getType() == "dividend":
                month_key = operation.timestamp.strftime("%Y-%m")
                dividends_by_month[month_key] += operation.getAmount()

        return dict(dividends_by_month)

    def get_stock_purchases_by_year(self) -> Dict[int, float]:
        """
        Calculate total stock purchases by year.

        Returns:
            Dictionary with year as key and total purchase amount as value
        """
        purchases_by_year = defaultdict(float)

        for operation in self.portfolio.cashOperations:
            if operation.getType() == "stock_purchase":
                year = operation.timestamp.year
                # Stock purchases are negative amounts, so we take absolute value
                purchases_by_year[year] += abs(operation.getAmount())

        return dict(purchases_by_year)

    def get_stock_purchases_by_month(self) -> Dict[str, float]:
        """
        Calculate total stock purchases by month (YYYY-MM format).

        Returns:
            Dictionary with month as key (YYYY-MM) and total purchase amount as value
        """
        purchases_by_month = defaultdict(float)

        for operation in self.portfolio.cashOperations:
            if operation.getType() == "stock_purchase":
                month_key = operation.timestamp.strftime("%Y-%m")
                # Stock purchases are negative amounts, so we take absolute value
                purchases_by_month[month_key] += abs(operation.getAmount())

        return dict(purchases_by_month)

    def get_all_statistics_by_year(self) -> Dict[str, Dict[int, float]]:
        """
        Get all statistics grouped by year.

        Returns:
            Dictionary containing all statistics by year
        """
        return {
            "deposits": self.get_deposits_by_year(),
            "dividends": self.get_dividends_by_year(),
            "stock_purchases": self.get_stock_purchases_by_year(),
        }

    def get_all_statistics_by_month(self) -> Dict[str, Dict[str, float]]:
        """
        Get all statistics grouped by month.

        Returns:
            Dictionary containing all statistics by month
        """
        return {
            "deposits": self.get_deposits_by_month(),
            "dividends": self.get_dividends_by_month(),
            "stock_purchases": self.get_stock_purchases_by_month(),
        }

    @abstractmethod
    def output_statistics(self, statistics: Dict[str, Any]) -> None:
        """
        Abstract method to output statistics.
        Implementation depends on the output format (console, file, database, etc.).

        Args:
            statistics: Dictionary containing the statistics to output
        """
        pass

    def generate_and_output_yearly_statistics(self) -> None:
        """
        Generate and output yearly statistics.
        """
        yearly_stats = self.get_all_statistics_by_year()
        self.output_statistics(yearly_stats)

    def generate_and_output_monthly_statistics(self) -> None:
        """
        Generate and output monthly statistics.
        """
        monthly_stats = self.get_all_statistics_by_month()
        self.output_statistics(monthly_stats)
