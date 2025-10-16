"""FastAPI application for Crossref academic search."""
import time
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.services.crossref_client import CrossrefClient
from app.services.search_service import SearchService
from app.services.export_service import ExportService
from app.utils.logger import configure_logging, get_logger

# Prometheus metrics
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


# Configure logging
configure_logging(settings.log_level)
logger = get_logger("app")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Define metrics
searches_total = Counter('searches_total', 'Total number of searches')
searches_errors_total = Counter(
    'searches_errors_total',
    'Total number of search errors',
    ['error_type']
)
exports_csv_total = Counter('exports_csv_total', 'Total CSV exports')
exports_bibtex_total = Counter('exports_bibtex_total', 'Total BibTeX exports')
search_duration_seconds = Histogram(
    'search_duration_seconds',
    'Search duration in seconds'
)
results_count = Histogram(
    'results_count',
    'Number of results per search',
    buckets=[0, 10, 30, 50, 100, 200, 500]
)

# Global service instances
crossref_client: CrossrefClient = None
search_service: SearchService = None
export_service: ExportService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown.
    """
    # Startup
    global crossref_client, search_service, export_service
    
    logger.info(
        "Starting application",
        user_agent=settings.app_user_agent,
        mailto=settings.app_mailto
    )
    
    # Initialize Crossref client
    crossref_client = CrossrefClient(
        user_agent=settings.app_user_agent,
        mailto=settings.app_mailto,
        timeout=settings.crossref_timeout
    )
    
    # Initialize services
    search_service = SearchService(crossref_client, logger)
    export_service = ExportService(crossref_client, logger)
    
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await crossref_client.close()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Crossref Academic Search",
    description="Search and export academic references from Crossref API",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all HTTP requests.
    """
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate latency
    latency_ms = (time.time() - start_time) * 1000
    
    # Log request
    logger.info(
        "HTTP request",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=round(latency_ms, 2)
    )
    
    return response


@app.get("/healthz")
async def healthcheck() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Status dictionary
    """
    return {"status": "ok"}


@app.get("/")
async def root():
    """
    Serve the main UI.
    
    Returns:
        HTML page
    """
    return FileResponse("app/static/index.html")


@app.get("/search")
@limiter.limit(settings.rate_limit_searches)
async def search_endpoint(
    request: Request,
    q: str,
    from_date: str = "2023-01-01",
    until_date: str = "2025-12-31",
    content_type: str = "journal-article",
    has_abstract: bool = True,
    rows: int = 30,
    max_results: int = 120,
    sort: str = "relevance",
) -> JSONResponse:
    """
    Search Crossref for academic references.
    
    Args:
        request: FastAPI request object (for rate limiting)
        q: Search query keywords (required)
        from_date: Start date filter (YYYY-MM-DD)
        until_date: End date filter (YYYY-MM-DD)
        content_type: Type of content (journal-article, proceedings-article, book-chapter)
        has_abstract: Whether to require abstract
        rows: Results per page (1-100)
        max_results: Maximum total results (1-500)
        sort: Sort order (relevance or published)
        
    Returns:
        JSON response with search results
    """
    from app.models import SearchFilters, ErrorResponse
    from app.utils.validators import ValidationError
    
    # Increment search counter
    searches_total.inc()
    
    try:
        # Create filters
        filters = SearchFilters(
            query=q,
            from_date=from_date,
            until_date=until_date,
            content_type=content_type,
            has_abstract=has_abstract,
            rows=rows,
            max_results=max_results,
            sort=sort
        )
        
        # Execute search with timing
        with search_duration_seconds.time():
            result = await search_service.search(q, filters)
        
        # Record results count
        results_count.observe(result.count)
        
        # Return results
        return JSONResponse(
            status_code=200,
            content=result.to_dict()
        )
        
    except ValidationError as e:
        # Validation error (400)
        searches_errors_total.labels(error_type='validation').inc()
        error_response = ErrorResponse(code=400, message=str(e))
        return JSONResponse(
            status_code=400,
            content=error_response.to_dict()
        )
        
    except Exception as e:
        # Check if it's a Crossref API error
        import httpx
        if isinstance(e, httpx.HTTPStatusError):
            status_code = e.response.status_code
            if status_code >= 500:
                # Crossref server error (503)
                searches_errors_total.labels(error_type='crossref_5xx').inc()
                error_response = ErrorResponse(
                    code=503,
                    message=f"Crossref API error: {str(e)}"
                )
                return JSONResponse(
                    status_code=503,
                    content=error_response.to_dict()
                )
            else:
                # Crossref client error (502)
                searches_errors_total.labels(error_type='crossref_4xx').inc()
                error_response = ErrorResponse(
                    code=502,
                    message=f"Crossref API error: {str(e)}"
                )
                return JSONResponse(
                    status_code=502,
                    content=error_response.to_dict()
                )
        
        # Internal server error (500)
        searches_errors_total.labels(error_type='internal').inc()
        logger.error(
            "Internal error in search endpoint",
            error=str(e),
            error_type=type(e).__name__
        )
        error_response = ErrorResponse(
            code=500,
            message="Internal server error"
        )
        return JSONResponse(
            status_code=500,
            content=error_response.to_dict()
        )


@app.get("/export/csv")
@limiter.limit(settings.rate_limit_exports)
async def export_csv_endpoint(
    request: Request,
    q: str,
    from_date: str = "2023-01-01",
    until_date: str = "2025-12-31",
    content_type: str = "journal-article",
    has_abstract: bool = True,
    rows: int = 30,
    max_results: int = 120,
    sort: str = "relevance",
):
    """
    Export search results to CSV.
    
    Uses same parameters as /search endpoint.
    
    Returns:
        CSV file download
    """
    from fastapi.responses import Response
    from app.models import SearchFilters, ErrorResponse
    from app.utils.validators import ValidationError
    
    try:
        # Create filters
        filters = SearchFilters(
            query=q,
            from_date=from_date,
            until_date=until_date,
            content_type=content_type,
            has_abstract=has_abstract,
            rows=rows,
            max_results=max_results,
            sort=sort
        )
        
        # Execute search
        result = await search_service.search(q, filters)
        
        # Generate CSV
        csv_content = export_service.export_csv(result.items)
        
        # Increment CSV export counter
        exports_csv_total.inc()
        
        # Return CSV file
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="crossref_results.csv"'
            }
        )
        
    except ValidationError as e:
        # Validation error (400)
        error_response = ErrorResponse(code=400, message=str(e))
        return JSONResponse(
            status_code=400,
            content=error_response.to_dict()
        )
        
    except Exception as e:
        # Internal server error (500)
        logger.error(
            "Internal error in CSV export endpoint",
            error=str(e),
            error_type=type(e).__name__
        )
        error_response = ErrorResponse(
            code=500,
            message="Internal server error"
        )
        return JSONResponse(
            status_code=500,
            content=error_response.to_dict()
        )



@app.get("/export/bibtex")
@limiter.limit(settings.rate_limit_exports)
async def export_bibtex_endpoint(
    request: Request,
    dois: str,
):
    """
    Export BibTeX entries for specified DOIs.
    
    Args:
        request: FastAPI request object (for rate limiting)
        dois: Comma-separated list of DOIs
        
    Returns:
        BibTeX file download
    """
    from fastapi.responses import Response
    from app.models import ErrorResponse
    
    try:
        # Validate DOIs parameter
        if not dois or not dois.strip():
            error_response = ErrorResponse(
                code=400,
                message="dois parameter is required"
            )
            return JSONResponse(
                status_code=400,
                content=error_response.to_dict()
            )
        
        # Parse DOIs (comma-separated)
        doi_list = [doi.strip() for doi in dois.split(',') if doi.strip()]
        
        if not doi_list:
            error_response = ErrorResponse(
                code=400,
                message="No valid DOIs provided"
            )
            return JSONResponse(
                status_code=400,
                content=error_response.to_dict()
            )
        
        # Generate BibTeX
        bibtex_content = await export_service.export_bibtex(doi_list)
        
        # Increment BibTeX export counter
        exports_bibtex_total.inc()
        
        # Return BibTeX file
        return Response(
            content=bibtex_content,
            media_type="text/plain",
            headers={
                "Content-Disposition": f'attachment; filename="crossref_references.bib"'
            }
        )
        
    except Exception as e:
        # Internal server error (500)
        logger.error(
            "Internal error in BibTeX export endpoint",
            error=str(e),
            error_type=type(e).__name__
        )
        error_response = ErrorResponse(
            code=500,
            message="Internal server error"
        )
        return JSONResponse(
            status_code=500,
            content=error_response.to_dict()
        )



@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    
    Returns:
        Metrics in Prometheus format
    """
    from fastapi.responses import Response
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
