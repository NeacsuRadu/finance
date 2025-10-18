from typing import List, Dict, Any, Type


class CsvColumn:
    """Represents a column definition in a CSV schema."""
    
    def __init__(self, name: str, column_type: Type, optional: bool = False):
        """
        Initialize a CSV column definition.
        
        Args:
            name: Column name
            column_type: Python type for the column (e.g., str, int, float, bool)
            optional: Whether the column can be empty/None
        """
        self.name = name
        self.column_type = column_type
        self.optional = optional
    
    def validate(self, value: Any) -> Any:
        """
        Validate and convert a value according to the column type.
        
        Args:
            value: The value to validate
            
        Returns:
            The converted value
            
        Raises:
            ValueError: If validation fails
        """
        if value is None or value == "":
            if self.optional:
                return None
            else:
                raise ValueError(f"Column '{self.name}' is required but got empty value")
        
        try:
            if self.column_type == bool:
                if isinstance(value, bool):
                    return value
                if isinstance(value, str):
                    if value.lower() in ('true', '1', 'yes', 'y'):
                        return True
                    elif value.lower() in ('false', '0', 'no', 'n'):
                        return False
                    else:
                        raise ValueError(f"Cannot convert '{value}' to bool")
                return bool(value)
            else:
                return self.column_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Column '{self.name}': Cannot convert '{value}' to {self.column_type.__name__}: {e}")


class CsvSchema:
    """Schema definition for CSV files with column validation."""
    
    def __init__(self, columns: List[CsvColumn]):
        """
        Initialize a CSV schema.
        
        Args:
            columns: List of CsvColumn objects defining the schema
        """
        self.columns = columns
        self.column_map: Dict[str, CsvColumn] = {col.name: col for col in columns}
    
    def validate_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and convert a row according to the schema.
        
        Args:
            row: Dictionary mapping column names to values
            
        Returns:
            Dictionary with validated and converted values
            
        Raises:
            ValueError: If validation fails
        """
        validated_row = {}
        
        # Validate each column in the schema
        for column in self.columns:
            if column.name not in row:
                if not column.optional:
                    raise ValueError(f"Required column '{column.name}' is missing from row")
                validated_row[column.name] = None
            else:
                validated_row[column.name] = column.validate(row[column.name])
        
        return validated_row
    
    def get_column_names(self) -> List[str]:
        """Get the list of column names in the schema."""
        return [col.name for col in self.columns]
