import csv
from typing import Dict, Any, Optional, List
from pathlib import Path

from .repository import Repository
from .csv_schema import CsvSchema


class LocalCsvRepository(Repository):
    """CSV-based repository implementation with schema validation."""
    
    def __init__(self, path: str, schema: CsvSchema):
        """
        Initialize the CSV repository.
        
        Args:
            path: Path to the CSV file
            schema: CsvSchema defining the expected structure
        """
        self.path = Path(path)
        self.schema = schema
        self.data: List[Dict[str, Any]] = []
    
    def load(self) -> None:
        """
        Load data from the CSV file and validate against schema.
        
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If any row fails schema validation
        """
        if not self.path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.path}")
        
        self.data = []
        
        with open(self.path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                # Validate the row against schema
                is_valid, errors = self.schema.validate_row(row)
                
                if not is_valid:
                    error_msg = f"Validation failed for row {row_num}:\n"
                    error_msg += "\n".join(f"  - {error}" for error in errors)
                    raise ValueError(error_msg)
                
                # Convert values to their proper types
                typed_row = self._convert_row_types(row)
                self.data.append(typed_row)
    
    def _convert_row_types(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert row values to their schema-defined types.
        
        Args:
            row: Raw row dictionary from CSV
            
        Returns:
            Dictionary with values converted to proper types
        """
        converted = {}
        
        for column_name, value in row.items():
            if column_name not in self.schema.column_map:
                # Keep unknown columns as-is
                converted[column_name] = value
                continue
            
            column = self.schema.column_map[column_name]
            
            # Handle empty values for optional columns
            if (value is None or value == '') and column.optional:
                converted[column_name] = None
                continue
            
            # Convert to the proper type
            try:
                if column.column_type == bool:
                    converted[column_name] = self._convert_to_bool(value)
                elif column.column_type in (int, float):
                    converted[column_name] = column.column_type(value)
                else:
                    converted[column_name] = value
            except (ValueError, TypeError):
                # If conversion fails, keep as string (validation should catch this)
                converted[column_name] = value
        
        return converted
    
    def _convert_to_bool(self, value: Any) -> bool:
        """Convert a value to boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes')
        return bool(value)
    
    def find(self, **filters) -> Optional[Dict[str, Any]]:
        """
        Find and return one row matching the given column-value filters.
        
        Args:
            **filters: Column-value pairs to filter by (e.g., id=123, name="John")
            
        Returns:
            Dictionary representing the first matching row, or None if not found
            
        Example:
            >>> repo.find(ticker="AAPL", date="2025-01-01")
        """
        for row in self.data:
            if self._matches_filters(row, filters):
                return row.copy()  # Return a copy to prevent external modifications
        
        return None
    
    def _matches_filters(self, row: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """
        Check if a row matches all the given filters.
        
        Args:
            row: Row to check
            filters: Dictionary of column-value pairs to match
            
        Returns:
            True if all filters match, False otherwise
        """
        for column, value in filters.items():
            if column not in row:
                return False
            
            # Compare values (handle type differences)
            row_value = row[column]
            
            # Convert both to strings for comparison if types differ
            if type(row_value) != type(value):
                if str(row_value) != str(value):
                    return False
            elif row_value != value:
                return False
        
        return True
