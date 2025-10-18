"""Subscription data models."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SubscriptionPlan(str, Enum):
    """Subscription plan types."""
    FREE = "free"
    PRO = "pro"
    TEAM = "team"
    ACADEMIC = "academic"
    INSTITUTIONAL = "institutional"


class SubscriptionStatus(str, Enum):
    """Subscription status types."""
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"


class Subscription(BaseModel):
    """Subscription model."""
    id: int
    user_id: int
    plan: SubscriptionPlan
    status: SubscriptionStatus
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SubscriptionResponse(BaseModel):
    """Subscription response model."""
    plan: SubscriptionPlan
    status: SubscriptionStatus
    current_period_end: Optional[datetime]
    cancel_at_period_end: bool
