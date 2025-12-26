"""Notifications routes."""
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Notification(BaseModel):
    id: str
    userId: str
    changeId: str
    message: str
    read: bool
    createdAt: str

@router.get("/", response_model=list[Notification])
async def get_notifications():
    """Get user notifications."""
    # TODO: Implement database query
    return []

@router.put("/{notification_id}/read", status_code=204)
async def mark_as_read(notification_id: str):
    """Mark notification as read."""
    # TODO: Implement database update
    pass
