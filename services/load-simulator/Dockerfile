# services/load-simulator/Dockerfile

FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM deps AS runtime
RUN addgroup --system --gid 1001 appgroup \
 && adduser  --system --uid 1001 --ingroup appgroup appuser
COPY --chown=appuser:appgroup . .
USER appuser

# No EXPOSE needed — simulator makes outbound requests, receives none
# No HEALTHCHECK — if it crashes, Docker restarts it (restart: unless-stopped)

CMD ["python", "-u", "main.py"]