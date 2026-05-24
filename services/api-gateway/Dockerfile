# services/api-gateway/Dockerfile

# ── Stage 1: base ──────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files (keeps image clean)
ENV PYTHONDONTWRITEBYTECODE=1
# Force stdout/stderr to be unbuffered (logs appear immediately)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ── Stage 2: dependencies ──────────────────────────────────────────────────────
FROM base AS deps

COPY requirements.txt .
# --no-cache-dir keeps the image smaller (no pip cache saved)
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 3: runtime ───────────────────────────────────────────────────────────
FROM deps AS runtime

# Security: create a non-root user — never run apps as root in containers
RUN addgroup --system --gid 1001 appgroup \
 && adduser  --system --uid 1001 --ingroup appgroup appuser

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

# Liveness check baked into the image — works without curl installed
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Use 2 workers for local dev; in K8s you control replicas instead
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]