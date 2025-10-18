"""Database connection and configuration."""
import os
from databases import Database
from sqlalchemy import create_engine, MetaData

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Database instance (will be None if DATABASE_URL not set)
database = None
metadata = MetaData()
engine = None

if DATABASE_URL:
    # Create database instance
    database = Database(DATABASE_URL)
    # Create engine for table creation
    engine = create_engine(DATABASE_URL)


async def connect_db():
    """Connect to database."""
    if database:
        await database.connect()


async def disconnect_db():
    """Disconnect from database."""
    if database:
        await database.disconnect()
