from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Repository(ABC):
    """Abstract interface for data repositories."""

    @abstractmethod
    def load(self) -> None:
        """
        Load data from the repository source.

        This method should load and validate data from the underlying storage.
        """
        pass

    @abstractmethod
    def find(self, **filters) -> Optional[Dict[str, Any]]:
        """
        Find a single row matching the given filters.

        Args:
            **filters: Column name and value pairs to filter by

        Returns:
            A dictionary representing the matching row, or None if no match found
        """
        pass

    @abstractmethod
    def create(self, items: List[Dict[str, Any]]) -> None:
        """
        Validates and inserts new items (rows) to the repository.
        Args:
            items: List of dicts to be validated and saved
        """
        pass
