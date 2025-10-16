"""Data normalization utilities for Crossref API responses."""
from typing import Dict, List, Optional, Any
import bleach
from app.models import NormalizedItem


class DataNormalizer:
    """Transforms Crossref API responses to consistent internal format."""
    
    # Allowed HTML tags for abstract sanitization
    ALLOWED_TAGS = ['p', 'br', 'i', 'b', 'em', 'strong']
    ALLOWED_ATTRIBUTES: Dict[str, List[str]] = {}
    
    @staticmethod
    def normalize_item(raw_item: Dict[str, Any]) -> NormalizedItem:
        """
        Normalize a Crossref item to internal format.
        
        Args:
            raw_item: Raw item from Crossref API response
            
        Returns:
            NormalizedItem with normalized fields
        """
        # Extract DOI
        doi = raw_item.get('DOI', '')
        
        # Extract title (first element of title array)
        title_list = raw_item.get('title', [])
        title = title_list[0] if title_list else 'No title'
        
        # Format authors
        authors_list = raw_item.get('author', [])
        authors = DataNormalizer.format_authors(authors_list)
        
        # Extract year
        year = DataNormalizer.extract_year(raw_item)
        
        # Extract journal (container-title or publisher as fallback)
        container_title = raw_item.get('container-title', [])
        journal = container_title[0] if container_title else raw_item.get('publisher', 'Unknown')
        
        # Clean abstract
        abstract = raw_item.get('abstract', '')
        if abstract:
            abstract = DataNormalizer.clean_abstract(abstract)
        else:
            abstract = 'No abstract available'
        
        # Construct URL
        url = f"https://doi.org/{doi}" if doi else ''
        
        return NormalizedItem(
            doi=doi,
            title=title,
            authors=authors,
            year=year,
            journal=journal,
            abstract=abstract,
            url=url
        )
    
    @staticmethod
    def clean_abstract(html_abstract: str) -> str:
        """
        Clean HTML from abstract, removing dangerous tags.
        
        Args:
            html_abstract: Abstract with HTML markup
            
        Returns:
            Sanitized abstract with only safe tags
        """
        cleaned = bleach.clean(
            html_abstract,
            tags=DataNormalizer.ALLOWED_TAGS,
            attributes=DataNormalizer.ALLOWED_ATTRIBUTES,
            strip=True
        )
        return cleaned.strip()
    
    @staticmethod
    def format_authors(authors_list: List[Dict[str, Any]]) -> str:
        """
        Format authors as 'Nombre Apellido; Nombre Apellido'.
        
        Args:
            authors_list: List of author dictionaries from Crossref
            
        Returns:
            Formatted author string
        """
        if not authors_list:
            return 'Unknown authors'
        
        formatted_authors = []
        for author in authors_list:
            given = author.get('given', '')
            family = author.get('family', '')
            
            # Construct full name
            if given and family:
                full_name = f"{given} {family}"
            elif family:
                full_name = family
            elif given:
                full_name = given
            else:
                continue
            
            formatted_authors.append(full_name)
        
        return '; '.join(formatted_authors) if formatted_authors else 'Unknown authors'
    
    @staticmethod
    def extract_year(raw_item: Dict[str, Any]) -> Optional[int]:
        """
        Extract publication year from date-parts.
        Prioritizes published-print, falls back to published-online.
        
        Args:
            raw_item: Raw item from Crossref API
            
        Returns:
            Publication year or None if not available
        """
        # Try published-print first
        published_print = raw_item.get('published-print', {})
        date_parts = published_print.get('date-parts', [])
        
        if date_parts and date_parts[0]:
            return date_parts[0][0]  # First element is the year
        
        # Fallback to published-online
        published_online = raw_item.get('published-online', {})
        date_parts = published_online.get('date-parts', [])
        
        if date_parts and date_parts[0]:
            return date_parts[0][0]
        
        # Try generic 'published' field
        published = raw_item.get('published', {})
        date_parts = published.get('date-parts', [])
        
        if date_parts and date_parts[0]:
            return date_parts[0][0]
        
        return None
