import csv
from typing import Any, Dict, List, Optional

from investments.repository.repository import Repository
from investments.repository.csv_schema import CsvSchema


class LocalCsvRepository(Repository):
    """Repository implementation for local CSV files with schema validation."""

    def __init__(self, path: str, schema: CsvSchema):
        """
        Initialize a local CSV repository.

        Args:
            path: Path to the CSV file
            schema: CsvSchema object defining the expected structure
        """
        self.path = path
        self.schema = schema
        self._data: List[Dict[str, Any]] = []

    def load(self) -> None:
        """
        Load data from the CSV file and validate against the schema.

        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If validation fails for any row
        """
        self._data = []

        with open(self.path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(
                reader, start=2
            ):  # Start at 2 (header is line 1)
                try:
                    validated_row = self.schema.validate_row(row)
                    self._data.append(validated_row)
                except ValueError as e:
                    raise ValueError(f"Validation error at row {row_num}: {e}")

    def find(self, **filters) -> Optional[Dict[str, Any]]:
        """
        Find a single row matching the given column filters.

        Args:
            **filters: Column name and value pairs to filter by
                      e.g., find(name="John", age=25)

        Returns:
            A dictionary representing the first matching row, or None if no match found
        """
        for row in self._data:
            match = True
            for column, value in filters.items():
                if column not in row or row[column] != value:
                    match = False
                    break

            if match:
                return row

        return None

    def find_all(self, **filters) -> List[Dict[str, Any]]:
        """
        Find all rows matching the given column filters.

        Args:
            **filters: Column name and value pairs to filter by

        Returns:
            A list of dictionaries representing all matching rows
        """
        results = []

        for row in self._data:
            match = True
            for column, value in filters.items():
                if column not in row or row[column] != value:
                    match = False
                    break

            if match:
                results.append(row)

        return results

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all loaded data.

        Returns:
            List of all rows in the repository
        """
        return self._data.copy()

    def create(self, items: List[Dict[str, Any]]) -> None:
        # Validate and add to memory
        rows_to_add = []
        for item in items:
            validated_row = self.schema.validate_row(item)
            rows_to_add.append(validated_row)

        # Append to in-memory
        self._data.extend(rows_to_add)

        # Append to file
        import os

        file_exists = os.path.exists(self.path)
        import csv

        with open(self.path, "a", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.schema.get_column_names())
            if not file_exists or os.path.getsize(self.path) == 0:
                writer.writeheader()
            for row in rows_to_add:
                writer.writerow(row)
