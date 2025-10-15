from investments.statistics import Statistics


class ConsoleStatistics(Statistics):
    """
    Concrete implementation of Statistics for console output.
    """

    def output_statistics(self, statistics: dict) -> None:
        """
        Output statistics to console with formatted display.

        Args:
            statistics: Dictionary containing the statistics to output
        """
        print("=" * 60)
        print("PORTFOLIO STATISTICS")
        print("=" * 60)

        # Output deposits
        if "deposits" in statistics and statistics["deposits"]:
            print("\nDEPOSITS:")
            print("-" * 20)
            for time_period, amount in sorted(statistics["deposits"].items()):
                print(f"{time_period}: €{amount:,.2f}")

        # Output dividends
        if "dividends" in statistics and statistics["dividends"]:
            print("\nDIVIDENDS:")
            print("-" * 20)
            for time_period, amount in sorted(statistics["dividends"].items()):
                print(f"{time_period}: €{amount:,.2f}")

        # Output stock purchases
        if "stock_purchases" in statistics and statistics["stock_purchases"]:
            print("\nSTOCK PURCHASES:")
            print("-" * 20)
            for time_period, amount in sorted(statistics["stock_purchases"].items()):
                print(f"{time_period}: €{amount:,.2f}")

        print("=" * 60)
