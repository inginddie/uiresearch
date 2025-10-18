"""User repository for database operations."""
from typing import Optional
from datetime import datetime
from app.database import database
from app.auth_models.user import User, UserCreate
from app.services.auth_service import hash_password


async def create_user(user_data: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        user_data: User creation data
        
    Returns:
        Created user
    """
    query = """
        INSERT INTO users (email, password_hash, full_name, created_at, updated_at)
        VALUES (:email, :password_hash, :full_name, :created_at, :updated_at)
        RETURNING id, email, full_name, is_active, is_verified, created_at, updated_at
    """
    
    now = datetime.utcnow()
    values = {
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
        "full_name": user_data.full_name,
        "created_at": now,
        "updated_at": now,
    }
    
    result = await database.fetch_one(query=query, values=values)
    return User(**dict(result))


async def get_user_by_email(email: str) -> Optional[dict]:
    """
    Get user by email (includes password hash).
    
    Args:
        email: User email
        
    Returns:
        User data with password hash or None
    """
    query = """
        SELECT id, email, password_hash, full_name, is_active, is_verified, created_at, updated_at
        FROM users
        WHERE email = :email
    """
    
    result = await database.fetch_one(query=query, values={"email": email})
    return dict(result) if result else None


async def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User or None
    """
    query = """
        SELECT id, email, full_name, is_active, is_verified, created_at, updated_at
        FROM users
        WHERE id = :user_id
    """
    
    result = await database.fetch_one(query=query, values={"user_id": user_id})
    return User(**dict(result)) if result else None


async def update_user_verification(user_id: int, is_verified: bool = True) -> None:
    """
    Update user verification status.
    
    Args:
        user_id: User ID
        is_verified: Verification status
    """
    query = """
        UPDATE users
        SET is_verified = :is_verified, updated_at = :updated_at
        WHERE id = :user_id
    """
    
    await database.execute(
        query=query,
        values={
            "user_id": user_id,
            "is_verified": is_verified,
            "updated_at": datetime.utcnow(),
        }
    )
