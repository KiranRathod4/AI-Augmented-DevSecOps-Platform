# services/api-gateway/main.py

import logging
import os
import time
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("api-gateway")

# ── Config ─────────────────────────────────────────────────────────────────────
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")

# ── Prometheus metrics ─────────────────────────────────────────────────────────
# Counter: increments only, never decreases — total requests seen
REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total number of HTTP requests through the API gateway",
    ["method", "endpoint", "http_status"],   # labels let you slice the metric
)

# Histogram: tracks distribution of latency values in configurable buckets
REQUEST_LATENCY = Histogram(
    "gateway_request_duration_seconds",
    "HTTP request latency through the API gateway",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5],
)

# ── App lifecycle ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API Gateway starting up")
    yield
    logger.info("API Gateway shutting down")

app = FastAPI(
    title="API Gateway",
    description="Single entry point — routes requests, exposes metrics",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Middleware: instrument every request ───────────────────────────────────────
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    # Normalise paths so /api/users/123 and /api/users/456 don't create
    # unbounded cardinality in Prometheus — label is the route pattern
    path = request.url.path

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=path,
        http_status=str(response.status_code),
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=path,
    ).observe(duration)

    # Add response time header so you can see it in curl output
    response.headers["X-Response-Time"] = f"{duration:.4f}s"
    return response

# ── Internal HTTP client helper ────────────────────────────────────────────────
async def proxy(method: str, url: str, **kwargs):
    """Shared helper that proxies to an upstream service."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, timeout=5.0, **kwargs)
            # Propagate the upstream status code transparently
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json().get("detail", "Upstream error"),
                )
            return response.json()
        except httpx.TimeoutException:
            logger.error(f"Timeout calling {url}")
            raise HTTPException(status_code=504, detail="Upstream service timed out") from None
        except httpx.RequestError as exc:
            logger.error(f"Cannot reach {url}: {exc}")
            raise HTTPException(status_code=503, detail="Upstream service unavailable") from exc

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["ops"])
async def health_check():
    """Liveness probe — Kubernetes will call this."""
    return {"status": "healthy", "service": "api-gateway", "version": "1.0.0"}

@app.get("/ready", tags=["ops"])
async def readiness_check():
    """
    Readiness probe — checks that upstream services are reachable.
    Kubernetes will not send traffic until this returns 200.
    """
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{USER_SERVICE_URL}/health", timeout=2.0)
            upstream_ok = r.status_code == 200
    except Exception:
        upstream_ok = False

    if not upstream_ok:
        raise HTTPException(status_code=503, detail="user-service not ready")
    return {"status": "ready", "upstreams": {"user-service": "ok"}}

@app.get("/metrics", tags=["ops"])
async def prometheus_metrics():
    """Prometheus scrape endpoint — returns all metrics in text format."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ── User routes (proxied to user-service) ──────────────────────────────────────
@app.get("/api/users", tags=["users"])
async def list_users():
    return await proxy("GET", f"{USER_SERVICE_URL}/users")

@app.get("/api/users/{user_id}", tags=["users"])
async def get_user(user_id: int):
    return await proxy("GET", f"{USER_SERVICE_URL}/users/{user_id}")

@app.post("/api/users", tags=["users"])
async def create_user(request: Request):
    body = await request.json()
    return await proxy("POST", f"{USER_SERVICE_URL}/users", json=body)

@app.delete("/api/users/{user_id}", tags=["users"])
async def delete_user(user_id: int):
    return await proxy("DELETE", f"{USER_SERVICE_URL}/users/{user_id}")
