"""
Test script to demonstrate statistics functionality using real XTB CSV data.
"""

import csv
from investments.portofolio import XtbPortofolio
from investments.console_statistics import ConsoleStatistics


def main():
    """Load XTB portfolio data and display statistics."""
    csv_file_path = "./tests/test_data/xtb.csv"

    try:
        print("Loading XTB portfolio data from CSV...")

        # Open and read the CSV file
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            portfolio = XtbPortofolio.createFromCsv(csv_reader)

        print("Portfolio loaded successfully!")
        print(f"Broker: {portfolio.get_broker_name()}")
        print(f"Total cash: €{portfolio.cash:,.2f}")
        print(f"Total transactions: {len(portfolio.get_transactions())}")
        print(f"Total cash operations: {len(portfolio.cashOperations)}")
        print(f"Number of positions: {len(portfolio.get_positions())}")
        print()

        # Display yearly statistics
        print("YEARLY STATISTICS:")
        print("=" * 60)
        yearly_stats = portfolio.get_statistics_by_year()
        portfolio.output_statistics(yearly_stats)
        print()

        # Display monthly statistics
        print("MONTHLY STATISTICS:")
        print("=" * 60)
        monthly_stats = portfolio.get_statistics_by_month()
        portfolio.output_statistics(monthly_stats)
        print()

        # Alternative: Using ConsoleStatistics class
        print("USING CONSOLE STATISTICS CLASS:")
        print("=" * 60)
        console_stats = ConsoleStatistics(portfolio)
        console_stats.generate_and_output_yearly_statistics()
        print()

        # Display some additional insights
        print("ADDITIONAL INSIGHTS:")
        print("=" * 60)

        # Find years with activity
        years_with_activity = set()
        for operation in portfolio.cashOperations:
            years_with_activity.add(operation.timestamp.year)

        print(f"Years with activity: {sorted(years_with_activity)}")

        # Find months with activity
        months_with_activity = set()
        for operation in portfolio.cashOperations:
            month_key = operation.timestamp.strftime("%Y-%m")
            months_with_activity.add(month_key)

        print(f"Months with activity: {len(months_with_activity)}")
        print(f"First activity: {min(months_with_activity)}")
        print(f"Latest activity: {max(months_with_activity)}")

        # Calculate totals
        total_deposits = sum(yearly_stats.get("deposits", {}).values())
        total_dividends = sum(yearly_stats.get("dividends", {}).values())
        total_purchases = sum(yearly_stats.get("stock_purchases", {}).values())

        print("\nTOTALS ACROSS ALL YEARS:")
        print(f"Total deposits: €{total_deposits:,.2f}")
        print(f"Total dividends: €{total_dividends:,.2f}")
        print(f"Total stock purchases: €{total_purchases:,.2f}")
        print(
            f"Net cash flow: €{total_deposits + total_dividends - total_purchases:,.2f}"
        )

    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {csv_file_path}")
    except Exception as e:
        print(f"Error loading portfolio: {e}")


if __name__ == "__main__":
    main()
