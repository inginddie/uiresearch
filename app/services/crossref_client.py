"""Crossref API client with pagination and retry logic."""
import httpx
from typing import List, Dict, Any, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


class CrossrefClient:
    """Client for interacting with Crossref API."""
    
    BASE_URL = "https://api.crossref.org/works"
    
    def __init__(self, user_agent: str, mailto: str, timeout: int = 30):
        """
        Initialize Crossref client.
        
        Args:
            user_agent: Application identifier
            mailto: Contact email for polite pool
            timeout: Request timeout in seconds
        """
        self.user_agent = user_agent
        self.mailto = mailto
        self.timeout = timeout
        
        # Configure headers for polite pool
        self.headers = {
            'User-Agent': f'{user_agent} (mailto:{mailto})'
        }
        
        # Create async HTTP client
        self.client = httpx.AsyncClient(
            headers=self.headers,
            timeout=timeout
        )
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def _build_filter_string(
        self,
        from_date: Optional[str] = None,
        until_date: Optional[str] = None,
        content_type: Optional[str] = None,
        has_abstract: bool = True
    ) -> str:
        """
        Build Crossref filter string.
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            until_date: End date in YYYY-MM-DD format
            content_type: Type of content (journal-article, etc.)
            has_abstract: Whether to require abstract
            
        Returns:
            Comma-separated filter string
        """
        filters = []
        
        if from_date:
            filters.append(f"from-pub-date:{from_date}")
        
        if until_date:
            filters.append(f"until-pub-date:{until_date}")
        
        if content_type:
            filters.append(f"type:{content_type}")
        
        if has_abstract:
            filters.append("has-abstract:true")
        
        return ','.join(filters)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((
            httpx.TimeoutException,
            httpx.HTTPStatusError,
        )),
        reraise=True,
    )
    async def _fetch_page(
        self,
        query: str,
        filter_str: str,
        rows: int,
        sort: str,
        cursor: str
    ) -> Dict[str, Any]:
        """
        Fetch a single page from Crossref API with retry logic.
        
        Args:
            query: Search query
            filter_str: Filter string
            rows: Number of results per page
            sort: Sort order
            cursor: Pagination cursor
            
        Returns:
            API response as dictionary
            
        Raises:
            httpx.HTTPStatusError: For HTTP errors
            httpx.TimeoutException: For timeouts
        """
        params = {
            'query': query,
            'rows': rows,
            'sort': sort,
            'cursor': cursor,
        }
        
        if filter_str:
            params['filter'] = filter_str
        
        response = await self.client.get(self.BASE_URL, params=params)
        
        # Raise for 4xx/5xx errors (will trigger retry for 5xx and 429)
        if response.status_code >= 400:
            # Don't retry on 4xx errors (except 429)
            if 400 <= response.status_code < 500 and response.status_code != 429:
                response.raise_for_status()
            # Retry on 5xx and 429
            response.raise_for_status()
        
        return response.json()
    
    async def search(
        self,
        query: str,
        from_date: Optional[str] = None,
        until_date: Optional[str] = None,
        content_type: str = "journal-article",
        has_abstract: bool = True,
        rows: int = 30,
        max_results: int = 120,
        sort: str = "relevance",
    ) -> List[Dict[str, Any]]:
        """
        Search Crossref with automatic pagination.
        
        Args:
            query: Search keywords
            from_date: Start date filter (YYYY-MM-DD)
            until_date: End date filter (YYYY-MM-DD)
            content_type: Type of content to search
            has_abstract: Whether to require abstract
            rows: Results per page (1-100)
            max_results: Maximum total results (1-500)
            sort: Sort order (relevance or published)
            
        Returns:
            List of raw items from Crossref
        """
        # Build filter string
        filter_str = self._build_filter_string(
            from_date=from_date,
            until_date=until_date,
            content_type=content_type,
            has_abstract=has_abstract
        )
        
        all_items: List[Dict[str, Any]] = []
        cursor = "*"  # Initial cursor
        
        while len(all_items) < max_results:
            # Fetch page
            response_data = await self._fetch_page(
                query=query,
                filter_str=filter_str,
                rows=rows,
                sort=sort,
                cursor=cursor
            )
            
            # Extract items
            message = response_data.get('message', {})
            items = message.get('items', [])
            
            if not items:
                # No more results
                break
            
            # Add items up to max_results
            remaining = max_results - len(all_items)
            all_items.extend(items[:remaining])
            
            # Check if we have more pages
            next_cursor = message.get('next-cursor')
            if not next_cursor or len(all_items) >= max_results:
                break
            
            cursor = next_cursor
        
        return all_items
    
    async def get_bibtex(self, doi: str) -> str:
        """
        Get BibTeX for a specific DOI via content negotiation.
        
        Args:
            doi: DOI to retrieve
            
        Returns:
            BibTeX entry as string
            
        Raises:
            httpx.HTTPStatusError: If DOI not found or error occurs
        """
        url = f"https://doi.org/{doi}"
        headers = {
            **self.headers,
            'Accept': 'application/x-bibtex'
        }
        
        response = await self.client.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        
        return response.text
