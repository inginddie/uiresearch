"""Validation utilities for search parameters."""
import re
from datetime import datetime
from typing import Any


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Validators:
    """Collection of validation functions for search parameters."""
    
    # Date format regex: YYYY-MM-DD
    DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    # Valid content types
    VALID_CONTENT_TYPES = {'journal-article', 'proceedings-article', 'book-chapter'}
    
    # Valid sort options
    VALID_SORT_OPTIONS = {'relevance', 'published'}
    
    @staticmethod
    def validate_date_format(date_str: str, field_name: str = "date") -> None:
        """
        Validate date format is YYYY-MM-DD.
        
        Args:
            date_str: Date string to validate
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If date format is invalid
        """
        if not Validators.DATE_PATTERN.match(date_str):
            raise ValidationError(
                f"{field_name} must be in YYYY-MM-DD format, got: {date_str}"
            )
        
        # Validate it's a real date
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            raise ValidationError(
                f"{field_name} is not a valid date: {date_str} - {str(e)}"
            )
    
    @staticmethod
    def validate_date_range(from_date: str, until_date: str) -> None:
        """
        Validate that from_date <= until_date.
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            until_date: End date in YYYY-MM-DD format
            
        Raises:
            ValidationError: If date range is invalid
        """
        # First validate formats
        Validators.validate_date_format(from_date, "from_date")
        Validators.validate_date_format(until_date, "until_date")
        
        # Parse dates
        from_dt = datetime.strptime(from_date, '%Y-%m-%d')
        until_dt = datetime.strptime(until_date, '%Y-%m-%d')
        
        # Validate range
        if from_dt > until_dt:
            raise ValidationError(
                f"from_date ({from_date}) must be <= until_date ({until_date})"
            )
    
    @staticmethod
    def validate_numeric_range(
        value: Any,
        min_val: int,
        max_val: int,
        field_name: str = "value"
    ) -> None:
        """
        Validate numeric value is within range.
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value (inclusive)
            max_val: Maximum allowed value (inclusive)
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If value is out of range or not numeric
        """
        # Check if numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"{field_name} must be numeric, got: {type(value).__name__}"
            )
        
        # Check if negative
        if value < 0:
            raise ValidationError(
                f"{field_name} cannot be negative, got: {value}"
            )
        
        # Check range
        if value < min_val or value > max_val:
            raise ValidationError(
                f"{field_name} must be between {min_val} and {max_val}, got: {value}"
            )
    
    @staticmethod
    def validate_enum(
        value: str,
        valid_values: set,
        field_name: str = "value"
    ) -> None:
        """
        Validate value is in set of valid options.
        
        Args:
            value: Value to validate
            valid_values: Set of valid values
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If value is not in valid set
        """
        if value not in valid_values:
            raise ValidationError(
                f"{field_name} must be one of {valid_values}, got: {value}"
            )
    
    @staticmethod
    def validate_content_type(content_type: str) -> None:
        """
        Validate content_type is valid.
        
        Args:
            content_type: Content type to validate
            
        Raises:
            ValidationError: If content type is invalid
        """
        Validators.validate_enum(
            content_type,
            Validators.VALID_CONTENT_TYPES,
            "content_type"
        )
    
    @staticmethod
    def validate_sort(sort: str) -> None:
        """
        Validate sort option is valid.
        
        Args:
            sort: Sort option to validate
            
        Raises:
            ValidationError: If sort option is invalid
        """
        Validators.validate_enum(
            sort,
            Validators.VALID_SORT_OPTIONS,
            "sort"
        )
    
    @staticmethod
    def validate_query(query: str) -> None:
        """
        Validate search query.
        
        Args:
            query: Search query to validate
            
        Raises:
            ValidationError: If query is invalid
        """
        if not query or not query.strip():
            raise ValidationError("query cannot be empty")
        
        if len(query) > 500:
            raise ValidationError(
                f"query cannot exceed 500 characters, got: {len(query)}"
            )
