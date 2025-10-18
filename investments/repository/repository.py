from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class Repository(ABC):
    """Abstract interface for data repositories."""
    
    @abstractmethod
    def load(self) -> None:
        """
        Load data from the repository source.
        
        This method should load and prepare data for querying.
        """
        pass
    
    @abstractmethod
    def find(self, **filters) -> Optional[Dict[str, Any]]:
        """
        Find a single row matching the given filters.
        
        Args:
            **filters: Column-value pairs to filter by (e.g., id=5, name='John')
            
        Returns:
            A dictionary representing the matching row, or None if not found
        """
        pass
