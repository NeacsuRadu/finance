import csv
from typing import List, Dict, Any, Optional

from investments.repository.repository import Repository
from investments.repository.csv_schema import CsvSchema


class LocalCsvRepository(Repository):
    """Repository implementation for CSV files with schema validation."""
    
    def __init__(self, path: str, schema: CsvSchema):
        """
        Initialize the CSV repository.
        
        Args:
            path: Path to the CSV file
            schema: CsvSchema object defining the expected structure
        """
        self.path = path
        self.schema = schema
        self.data: List[Dict[str, Any]] = []
    
    def load(self) -> None:
        """
        Load data from the CSV file and validate against the schema.
        
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If validation fails
        """
        self.data = []
        
        with open(self.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                try:
                    validated_row = self.schema.validate_row(row)
                    self.data.append(validated_row)
                except ValueError as e:
                    raise ValueError(f"Validation error at row {row_num}: {e}")
    
    def find(self, **filters) -> Optional[Dict[str, Any]]:
        """
        Find a single row matching the given filters.
        
        Args:
            **filters: Column-value pairs to filter by (e.g., id=5, name='John')
            
        Returns:
            A dictionary representing the first matching row, or None if not found
            
        Example:
            repository.find(name='John', age=30)
        """
        for row in self.data:
            match = True
            for column, value in filters.items():
                if column not in row or row[column] != value:
                    match = False
                    break
            
            if match:
                return row.copy()  # Return a copy to prevent external modifications
        
        return None
    
    def find_all(self, **filters) -> List[Dict[str, Any]]:
        """
        Find all rows matching the given filters.
        
        Args:
            **filters: Column-value pairs to filter by
            
        Returns:
            A list of dictionaries representing all matching rows
        """
        results = []
        
        for row in self.data:
            match = True
            for column, value in filters.items():
                if column not in row or row[column] != value:
                    match = False
                    break
            
            if match:
                results.append(row.copy())
        
        return results
