"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
import os

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    company: str = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    permissions: list[str]

class LoginResponse(BaseModel):
    token: str
    user: UserResponse
    expiresIn: int

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user with email and password."""
    # TODO: Implement database lookup and password verification
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register", status_code=201)
async def register(request: RegisterRequest):
    """Create new user account."""
    # TODO: Implement user creation with password hashing
    return {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "email": request.email,
        "name": request.name,
        "company": request.company,
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
