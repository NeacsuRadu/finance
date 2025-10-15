from abc import ABC, abstractmethod
from typing import Dict, Any


class Portofolio(ABC):
    """
    Base portfolio class for managing investments.
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_statistics_by_year(self) -> Dict[str, Dict[int, float]]:
        """
        Get portfolio statistics grouped by year.

        Returns:
            Dictionary containing statistics by year
        """
        pass

    @abstractmethod
    def get_statistics_by_month(self) -> Dict[str, Dict[str, float]]:
        """
        Get portfolio statistics grouped by month.

        Returns:
            Dictionary containing statistics by month
        """
        pass

    @abstractmethod
    def output_statistics(self, statistics: Dict[str, Any]) -> None:
        """
        Abstract method to output statistics.
        Implementation depends on the output format (console, file, database, etc.).

        Args:
            statistics: Dictionary containing the statistics to output
        """
        pass
