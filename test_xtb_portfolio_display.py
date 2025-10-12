"""
Test script to load XTB portfolio data from CSV and display comprehensive portfolio information.
"""

import csv
from investments.portofolio import XtbPortofolio


def format_currency(amount):
    """Format amount as currency with proper sign."""
    return f"€{amount:,.2f}"


def format_timestamp(timestamp):
    """Format timestamp for display."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def display_portfolio_summary(portfolio):
    """Display a comprehensive summary of the portfolio."""
    print("=" * 80)
    print(f"PORTFOLIO SUMMARY - {portfolio.get_broker_name()}")
    print("=" * 80)

    # Basic portfolio info
    summary = portfolio.get_portfolio_summary()
    print(f"Total Cash: {format_currency(summary['total_cash'])}")
    print(f"Number of Positions: {summary['positions_count']}")
    print(f"Number of Symbols: {len(summary['symbols'])}")
    print(f"Total Transactions: {len(portfolio.get_transactions())}")
    print()


def display_cash_operations(portfolio):
    """Display cash operations summary."""
    print("CASH OPERATIONS SUMMARY")
    print("-" * 40)

    cash_summary = portfolio.get_cash_operations_summary()

    print(f"Total Operations: {cash_summary['total_operations']}")
    print()

    # Operations by type
    print("Operations by Type:")
    for op_type, data in cash_summary["operations_by_type"].items():
        print(
            f"  {op_type}: {data['count']} operations, Total: {format_currency(data['total_amount'])}"
        )
    print()

    # Recent operations (last 10)
    print("Recent Operations (last 10):")
    recent_ops = sorted(
        cash_summary["operations"], key=lambda x: x["timestamp"], reverse=True
    )[:10]
    for op in recent_ops:
        print(
            f"  {format_timestamp(op['timestamp'])} | {op['type']} | {format_currency(op['amount'])}"
        )
    print()


def display_symbols_and_transactions(portfolio):
    """Display symbols and their transactions."""
    print("SYMBOLS AND TRANSACTIONS")
    print("-" * 40)

    symbols = portfolio.get_symbols()

    if not symbols:
        print("No symbols found in portfolio.")
        return

    for symbol in sorted(symbols):
        transactions = portfolio.get_symbol_transactions(symbol)
        print(f"\nSymbol: {symbol}")
        print(f"  Transactions: {len(transactions)}")

        if transactions:
            # Calculate total amount for this symbol
            total_amount = sum(t["amount"] for t in transactions)
            print(f"  Total Amount: {format_currency(total_amount)}")

            # Show transaction types for this symbol
            types = {}
            for t in transactions:
                t_type = t["type"]
                if t_type not in types:
                    types[t_type] = 0
                types[t_type] += 1

            print(
                f"  Transaction Types: {', '.join(f'{t_type}({count})' for t_type, count in types.items())}"
            )

            # Show recent transactions for this symbol (last 5)
            recent_transactions = sorted(
                transactions, key=lambda x: x["time"], reverse=True
            )[:5]
            print("  Recent Transactions:")
            for t in recent_transactions:
                print(
                    f"    {format_timestamp(t['time'])} | {t['type']} | {format_currency(t['amount'])}"
                )
                if t["comment"]:
                    print(f"      Comment: {t['comment']}")
    print()


def display_transaction_types_summary(portfolio):
    """Display summary by transaction types."""
    print("TRANSACTION TYPES SUMMARY")
    print("-" * 40)

    transactions = portfolio.get_transactions()
    type_summary = {}

    for t in transactions:
        t_type = t["type"]
        if t_type not in type_summary:
            type_summary[t_type] = {"count": 0, "total_amount": 0, "symbols": set()}

        type_summary[t_type]["count"] += 1
        type_summary[t_type]["total_amount"] += t["amount"]
        if t["symbol"]:
            type_summary[t_type]["symbols"].add(t["symbol"])

    for t_type, data in sorted(type_summary.items()):
        print(f"{t_type}:")
        print(f"  Count: {data['count']}")
        print(f"  Total Amount: {format_currency(data['total_amount'])}")
        if data["symbols"]:
            symbols_list = sorted(list(data["symbols"]))
            print(f"  Symbols: {', '.join(symbols_list)}")
        print()


def main():
    """Main function to load and display XTB portfolio data."""
    csv_file_path = "./tests/test_data/xtb.csv"

    try:
        print("Loading XTB portfolio data...")

        # Open and read the CSV file
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            portfolio = XtbPortofolio.createFromCsv(csv_reader)

        print("Portfolio loaded successfully!")
        print()

        # Display all portfolio information
        display_portfolio_summary(portfolio)
        display_cash_operations(portfolio)
        display_symbols_and_transactions(portfolio)
        display_transaction_types_summary(portfolio)

        print("=" * 80)
        print("PORTFOLIO ANALYSIS COMPLETE")
        print("=" * 80)

    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {csv_file_path}")
    except Exception as e:
        print(f"Error loading portfolio: {e}")


if __name__ == "__main__":
    main()
