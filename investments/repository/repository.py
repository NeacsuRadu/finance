from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Repository(ABC):
    """Abstract interface for data repositories."""
    
    @abstractmethod
    def load(self) -> None:
        """
        Load data from the repository source.
        
        Implementations should load data into internal storage and validate it.
        """
        pass
    
    @abstractmethod
    def find(self, **filters) -> Optional[Dict[str, Any]]:
        """
        Find and return one row matching the given filters.
        
        Args:
            **filters: Column-value pairs to filter by (e.g., id=123, name="John")
            
        Returns:
            Dictionary representing the matching row, or None if not found
        """
        pass
