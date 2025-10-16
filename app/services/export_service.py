"""Export service for generating CSV and BibTeX exports."""
import csv
import io
from typing import List, Any
import structlog

from app.models import NormalizedItem
from app.services.crossref_client import CrossrefClient


class ExportService:
    """Handles export operations in different formats."""
    
    def __init__(self, crossref_client: CrossrefClient = None, logger: Any = None):
        """
        Initialize export service.
        
        Args:
            crossref_client: Crossref client for BibTeX export (optional)
            logger: Structured logger (optional)
        """
        self.crossref_client = crossref_client
        self.logger = logger or structlog.get_logger()
    
    def export_csv(self, items: List[NormalizedItem]) -> str:
        """
        Generate CSV export from normalized items.
        
        Args:
            items: List of normalized items to export
            
        Returns:
            CSV content as string with UTF-8 BOM
        """
        # Create string buffer
        output = io.StringIO()
        
        # Add UTF-8 BOM for Excel compatibility
        output.write('\ufeff')
        
        # Define CSV columns
        fieldnames = ['doi', 'title', 'authors', 'year', 'journal', 'abstract', 'url']
        
        # Create CSV writer
        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n'
        )
        
        # Write header
        writer.writeheader()
        
        # Write rows
        for item in items:
            row = item.to_dict()
            
            # Replace newlines in abstract with space
            if row.get('abstract'):
                row['abstract'] = row['abstract'].replace('\n', ' ').replace('\r', ' ')
            
            # Handle None values
            row = {k: (v if v is not None else '') for k, v in row.items()}
            
            writer.writerow(row)
        
        # Get CSV content
        csv_content = output.getvalue()
        output.close()
        
        self.logger.info(
            "CSV export generated",
            items_count=len(items)
        )
        
        return csv_content
    
    async def export_bibtex(self, dois: List[str]) -> str:
        """
        Get BibTeX entries for multiple DOIs.
        
        Args:
            dois: List of DOIs to retrieve
            
        Returns:
            Concatenated BibTeX entries
            
        Raises:
            ValueError: If crossref_client is not configured
        """
        if not self.crossref_client:
            raise ValueError("CrossrefClient is required for BibTeX export")
        
        bibtex_entries = []
        failed_dois = []
        
        for doi in dois:
            try:
                bibtex = await self.crossref_client.get_bibtex(doi)
                bibtex_entries.append(bibtex.strip())
                
                self.logger.debug(
                    "BibTeX retrieved",
                    doi=doi
                )
                
            except Exception as e:
                # Log error but continue with other DOIs
                self.logger.warning(
                    "Failed to retrieve BibTeX",
                    doi=doi,
                    error=str(e),
                    error_type=type(e).__name__
                )
                failed_dois.append(doi)
        
        # Concatenate entries with double newline
        result = '\n\n'.join(bibtex_entries)
        
        self.logger.info(
            "BibTeX export completed",
            total_dois=len(dois),
            successful=len(bibtex_entries),
            failed=len(failed_dois)
        )
        
        return result
