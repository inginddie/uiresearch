"""Data models for the application."""
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


@dataclass
class NormalizedItem:
    """Represents a normalized academic reference."""
    
    doi: str
    title: str
    authors: str  # "Nombre Apellido; Nombre Apellido"
    year: Optional[int]
    journal: str
    abstract: str
    url: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class SearchFilters:
    """Validated search parameters."""
    
    query: str
    from_date: str = "2023-01-01"
    until_date: str = "2025-12-31"
    content_type: str = "journal-article"
    has_abstract: bool = True
    rows: int = 30
    max_results: int = 120
    sort: str = "relevance"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class SearchResult:
    """Result of a search operation."""
    
    count: int
    items: List[NormalizedItem]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            'count': self.count,
            'items': [item.to_dict() for item in self.items],
        }


@dataclass
class ErrorResponse:
    """Structured error response."""
    
    code: int
    message: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            'error': {
                'code': self.code,
                'message': self.message,
            }
        }
