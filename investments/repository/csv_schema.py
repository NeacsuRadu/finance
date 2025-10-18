from typing import List, Dict, Any, Type


class Column:
    """Represents a column definition in a CSV schema."""
    
    def __init__(self, name: str, type: Type, optional: bool = False):
        """
        Initialize a column definition.
        
        Args:
            name: The name of the column
            type: The Python type for this column (e.g., str, int, float)
            optional: Whether this column is optional (default: False)
        """
        self.name = name
        self.type = type
        self.optional = optional
    
    def validate(self, value: Any) -> Any:
        """
        Validate and convert a value according to the column's type.
        
        Args:
            value: The value to validate
            
        Returns:
            The converted value
            
        Raises:
            ValueError: If the value cannot be converted to the expected type
        """
        if value is None or value == '':
            if self.optional:
                return None
            else:
                raise ValueError(f"Column '{self.name}' is required but got empty value")
        
        try:
            if self.type == bool:
                # Handle boolean conversion from string
                if isinstance(value, str):
                    if value.lower() in ('true', '1', 'yes'):
                        return True
                    elif value.lower() in ('false', '0', 'no'):
                        return False
                    else:
                        raise ValueError(f"Cannot convert '{value}' to boolean")
                return bool(value)
            else:
                return self.type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Column '{self.name}': cannot convert '{value}' to {self.type.__name__}: {e}")


class CsvSchema:
    """Schema definition for CSV files with column types and validation."""
    
    def __init__(self, columns: List[Column]):
        """
        Initialize a CSV schema with column definitions.
        
        Args:
            columns: List of Column objects defining the schema
        """
        self.columns = columns
        self.column_map = {col.name: col for col in columns}
    
    def validate_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a row against the schema.
        
        Args:
            row: Dictionary representing a CSV row
            
        Returns:
            Dictionary with validated and converted values
            
        Raises:
            ValueError: If validation fails
        """
        validated_row = {}
        
        # Check for required columns
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
