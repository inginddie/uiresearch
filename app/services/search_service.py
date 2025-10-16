"""Search service for orchestrating Crossref searches."""
from typing import Any
import structlog

from app.models import SearchFilters, SearchResult, NormalizedItem
from app.services.crossref_client import CrossrefClient
from app.utils.normalizer import DataNormalizer
from app.utils.validators import Validators, ValidationError


class SearchService:
    """Orchestrates search operations with validation and logging."""
    
    def __init__(self, crossref_client: CrossrefClient, logger: Any = None):
        """
        Initialize search service.
        
        Args:
            crossref_client: Crossref API client
            logger: Structured logger (optional)
        """
        self.crossref_client = crossref_client
        self.logger = logger or structlog.get_logger()
    
    def validate_filters(self, filters: SearchFilters) -> None:
        """
        Validate search filters.
        
        Args:
            filters: Search filters to validate
            
        Raises:
            ValidationError: If any filter is invalid
        """
        # Validate query
        Validators.validate_query(filters.query)
        
        # Validate date range
        Validators.validate_date_range(filters.from_date, filters.until_date)
        
        # Validate rows
        Validators.validate_numeric_range(
            filters.rows,
            min_val=1,
            max_val=100,
            field_name="rows"
        )
        
        # Validate max_results
        Validators.validate_numeric_range(
            filters.max_results,
            min_val=1,
            max_val=500,
            field_name="max_results"
        )
        
        # Validate content_type
        Validators.validate_content_type(filters.content_type)
        
        # Validate sort
        Validators.validate_sort(filters.sort)
    
    async def search(
        self,
        query: str,
        filters: SearchFilters,
    ) -> SearchResult:
        """
        Execute search with validation and logging.
        
        Args:
            query: Search query (for logging, already in filters)
            filters: Validated search filters
            
        Returns:
            SearchResult with normalized items
            
        Raises:
            ValidationError: If filters are invalid
            Exception: For other errors during search
        """
        # Validate filters
        self.validate_filters(filters)
        
        # Log search start
        self.logger.info(
            "Search started",
            query=filters.query,
            from_date=filters.from_date,
            until_date=filters.until_date,
            content_type=filters.content_type,
            has_abstract=filters.has_abstract,
            rows=filters.rows,
            max_results=filters.max_results,
            sort=filters.sort
        )
        
        try:
            # Execute search via Crossref client
            raw_items = await self.crossref_client.search(
                query=filters.query,
                from_date=filters.from_date,
                until_date=filters.until_date,
                content_type=filters.content_type,
                has_abstract=filters.has_abstract,
                rows=filters.rows,
                max_results=filters.max_results,
                sort=filters.sort
            )
            
            # Normalize items
            normalized_items = []
            for raw_item in raw_items:
                try:
                    normalized = DataNormalizer.normalize_item(raw_item)
                    normalized_items.append(normalized)
                except Exception as e:
                    # Log normalization error but continue
                    self.logger.warning(
                        "Failed to normalize item",
                        error=str(e),
                        doi=raw_item.get('DOI', 'unknown')
                    )
            
            # Create result
            result = SearchResult(
                count=len(normalized_items),
                items=normalized_items
            )
            
            # Log success
            self.logger.info(
                "Search completed",
                query=filters.query,
                results_count=result.count,
                pages_fetched=(len(raw_items) + filters.rows - 1) // filters.rows
            )
            
            return result
            
        except Exception as e:
            # Log error
            self.logger.error(
                "Search failed",
                query=filters.query,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
