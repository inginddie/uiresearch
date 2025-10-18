"""Database connection and configuration."""
import os
from databases import Database
from sqlalchemy import create_engine, MetaData

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Create database instance
database = Database(DATABASE_URL)

# Create SQLAlchemy metadata
metadata = MetaData()

# Create engine for table creation
engine = create_engine(DATABASE_URL)


async def connect_db():
    """Connect to database."""
    await database.connect()


async def disconnect_db():
    """Disconnect from database."""
    await database.disconnect()
