from typing import List, Dict, Any


class CsvColumn:
    """Represents a column definition in a CSV schema."""
    
    def __init__(self, name: str, column_type: type, optional: bool = False):
        """
        Initialize a CSV column definition.
        
        Args:
            name: Column name
            column_type: Expected type of the column (e.g., str, int, float)
            optional: Whether the column can be empty/missing
        """
        self.name = name
        self.column_type = column_type
        self.optional = optional
    
    def validate(self, value: Any) -> bool:
        """
        Validate a value against this column's type.
        
        Args:
            value: Value to validate
            
        Returns:
            True if value is valid, False otherwise
        """
        if value is None or value == '':
            return self.optional
        
        try:
            if self.column_type == bool:
                # Handle boolean conversion
                if isinstance(value, bool):
                    return True
                if isinstance(value, str):
                    return value.lower() in ('true', 'false', '1', '0', 'yes', 'no')
                return False
            elif self.column_type in (int, float):
                # Try to convert to the expected numeric type
                self.column_type(value)
                return True
            elif self.column_type == str:
                return True
            else:
                # For other types, check if it's an instance
                return isinstance(value, self.column_type)
        except (ValueError, TypeError):
            return False


class CsvSchema:
    """Defines the schema for a CSV file."""
    
    def __init__(self, columns: List[CsvColumn]):
        """
        Initialize a CSV schema.
        
        Args:
            columns: List of CsvColumn definitions
        """
        self.columns = columns
        self.column_map: Dict[str, CsvColumn] = {col.name: col for col in columns}
    
    def validate_row(self, row: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate a row against the schema.
        
        Args:
            row: Dictionary representing a CSV row
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for required columns
        for column in self.columns:
            if column.name not in row:
                if not column.optional:
                    errors.append(f"Missing required column: {column.name}")
            else:
                value = row[column.name]
                if not column.validate(value):
                    errors.append(
                        f"Invalid value for column '{column.name}': "
                        f"expected {column.column_type.__name__}, got '{value}'"
                    )
        
        return len(errors) == 0, errors
    
    def get_column_names(self) -> List[str]:
        """Get list of all column names in the schema."""
        return [col.name for col in self.columns]
