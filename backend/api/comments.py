"""Comments routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class CommentRequest(BaseModel):
    content: str

class Comment(CommentRequest):
    id: str
    changeId: str
    userId: str
    createdAt: str

@router.post("/{change_id}/comments", response_model=Comment, status_code=201)
async def add_comment(change_id: str, request: CommentRequest):
    """Add comment to schema change."""
    # TODO: Implement database insert
    return {
        **request.dict(),
        "id": "comment-id",
        "changeId": change_id,
        "userId": "user-id",
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/{change_id}/comments", response_model=list[Comment])
async def get_comments(change_id: str):
    """Get all comments for a schema change."""
    # TODO: Implement database query
    return []
