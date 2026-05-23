# services/user-service/main.py

import logging
import time
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import User

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("user-service")

# ── Prometheus metrics ─────────────────────────────────────────────────────────
USERS_CREATED_TOTAL = Counter(
    "user_service_users_created_total",
    "Total number of users successfully created",
)
USERS_DELETED_TOTAL = Counter(
    "user_service_users_deleted_total",
    "Total number of users deleted",
)
REQUEST_COUNT = Counter(
    "user_service_requests_total",
    "Total HTTP requests to user-service",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "user_service_request_duration_seconds",
    "HTTP request latency for user-service",
    ["endpoint"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
)
# Gauge: can go up AND down — represents a current snapshot
ACTIVE_USERS_GAUGE = Gauge(
    "user_service_active_users",
    "Current number of users in the database",
)

# ── Pydantic schemas ───────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name cannot be empty")
        if len(v) > 100:
            raise ValueError("name must be 100 characters or fewer")
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

    @classmethod
    def from_orm_user(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at.isoformat(),
        )

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int

# ── App ────────────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("User Service starting — initialising database")
    init_db()
    logger.info("User Service ready")
    yield
    logger.info("User Service shutting down")

app = FastAPI(
    title="User Service",
    description="Owns user data, backed by PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=str(response.status_code),
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
    return response

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["ops"])
async def health():
    return {"status": "healthy", "service": "user-service", "version": "1.0.0"}

@app.get("/metrics", tags=["ops"])
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/users", response_model=UserListResponse, tags=["users"])
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    # Update the gauge every time we query — keeps it in sync
    ACTIVE_USERS_GAUGE.set(len(users))
    return UserListResponse(
        users=[UserResponse.from_orm_user(u) for u in users],
        total=len(users),
    )

@app.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserResponse.from_orm_user(user)

@app.post("/users", response_model=UserResponse, status_code=201, tags=["users"])
async def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=payload.name, email=payload.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"A user with email '{payload.email}' already exists",
        )

    USERS_CREATED_TOTAL.inc()
    ACTIVE_USERS_GAUGE.inc()
    logger.info(f"Created user id={db_user.id} email={db_user.email}")
    return UserResponse.from_orm_user(db_user)

@app.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    db.delete(user)
    db.commit()
    USERS_DELETED_TOTAL.inc()
    ACTIVE_USERS_GAUGE.dec()
    logger.info(f"Deleted user id={user_id}")
    return {"message": f"User {user_id} deleted successfully"}