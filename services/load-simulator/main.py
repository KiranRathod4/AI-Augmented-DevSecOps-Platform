# services/load-simulator/main.py

import asyncio
import logging
import os
import random

import httpx

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | simulator | %(message)s",
)
logger = logging.getLogger("load-simulator")

# ── Config ─────────────────────────────────────────────────────────────────────
GATEWAY_URL      = os.getenv("GATEWAY_URL", "http://api-gateway:8000")
BASE_INTERVAL    = float(os.getenv("REQUEST_INTERVAL", "0.8"))   # seconds between requests
STARTUP_DELAY    = int(os.getenv("STARTUP_DELAY", "8"))           # wait for gateway to be ready
MAX_STORED_IDS   = 50                                              # remember last N created user ids

# ── Sample data ────────────────────────────────────────────────────────────────
FIRST_NAMES = [
    "Aarav", "Priya", "Rohit", "Sneha", "Arjun", "Divya",
    "Karthik", "Meera", "Vikram", "Ananya", "Rahul", "Pooja",
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank",
]
DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "devops.io", "example.org"]

# Circular buffer of user IDs we have created — so we can GET them too
created_ids: list[int] = []

def random_email(name: str) -> str:
    suffix = random.randint(100, 9999)
    domain = random.choice(DOMAINS)
    return f"{name.lower().replace(' ', '.')}{suffix}@{domain}"

# ── Traffic actions ────────────────────────────────────────────────────────────
async def action_create_user(client: httpx.AsyncClient) -> None:
    name = random.choice(FIRST_NAMES) + " " + random.choice(FIRST_NAMES)
    payload = {"name": name, "email": random_email(name)}
    try:
        r = await client.post(f"{GATEWAY_URL}/api/users", json=payload, timeout=5.0)
        if r.status_code == 201:
            user_id = r.json()["id"]
            created_ids.append(user_id)
            if len(created_ids) > MAX_STORED_IDS:
                created_ids.pop(0)
            logger.info(f"CREATE  user id={user_id} name='{name}'  ✓")
        elif r.status_code == 409:
            logger.debug("CREATE  duplicate email, skipped")
        else:
            logger.warning(f"CREATE  unexpected status {r.status_code}")
    except Exception as e:
        logger.error(f"CREATE  failed: {e}")

async def action_list_users(client: httpx.AsyncClient) -> None:
    try:
        r = await client.get(f"{GATEWAY_URL}/api/users", timeout=5.0)
        count = r.json().get("total", "?") if r.status_code == 200 else "err"
        logger.info(f"LIST    /api/users  status={r.status_code}  total={count}")
    except Exception as e:
        logger.error(f"LIST    failed: {e}")

async def action_get_user(client: httpx.AsyncClient) -> None:
    if not created_ids:
        logger.debug("GET single — no ids yet, skipping")
        return
    user_id = random.choice(created_ids)
    try:
        r = await client.get(f"{GATEWAY_URL}/api/users/{user_id}", timeout=5.0)
        logger.info(f"GET     /api/users/{user_id}  status={r.status_code}")
    except Exception as e:
        logger.error(f"GET     user {user_id} failed: {e}")

async def action_health_check(client: httpx.AsyncClient) -> None:
    try:
        r = await client.get(f"{GATEWAY_URL}/health", timeout=3.0)
        logger.info(f"HEALTH  /health  status={r.status_code}")
    except Exception as e:
        logger.error(f"HEALTH  failed: {e}")

async def action_readiness_check(client: httpx.AsyncClient) -> None:
    try:
        r = await client.get(f"{GATEWAY_URL}/ready", timeout=3.0)
        logger.info(f"READY   /ready  status={r.status_code}")
    except Exception as e:
        logger.error(f"READY   failed: {e}")

# ── Weighted action table ──────────────────────────────────────────────────────
# (action_fn, probability_weight)
ACTIONS = [
    (action_create_user,    0.25),   # 25% of traffic
    (action_list_users,     0.35),   # 35% — most common call
    (action_get_user,       0.25),   # 25%
    (action_health_check,   0.10),   # 10%
    (action_readiness_check, 0.05),  # 5%
]

# ── Main loop ──────────────────────────────────────────────────────────────────
async def run():
    logger.info(f"Load simulator starting. Target: {GATEWAY_URL}")
    logger.info(f"Waiting {STARTUP_DELAY}s for services to start...")
    await asyncio.sleep(STARTUP_DELAY)
    logger.info("Starting traffic generation")

    fns     = [fn for fn, _ in ACTIONS]
    weights = [w  for _,  w in ACTIONS]

    async with httpx.AsyncClient() as client:
        while True:
            action = random.choices(fns, weights=weights, k=1)[0]
            await action(client)

            # Jitter: vary interval slightly so requests don't arrive in lockstep
            jitter = random.uniform(-0.2, 0.4)
            await asyncio.sleep(max(0.1, BASE_INTERVAL + jitter))

if __name__ == "__main__":
    asyncio.run(run())
