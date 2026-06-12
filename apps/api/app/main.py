import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import text

from .config import get_settings
from .database import create_db_and_tables, engine
from .exceptions import AppError
from .logging_config import setup_logging
from .middleware import RequestIdMiddleware
from .routers import auth, content, jobs, settings, tasks, webhooks

setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("action_engine")

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ALEMBIC_MIGRATIONS_RUN") != "1":
        create_db_and_tables()
        logger.info("Database tables created via create_all (dev mode).")
    yield


app = FastAPI(title="Action Engine API", version="0.2.0", lifespan=lifespan, state={"limiter": limiter})
settings_obj = get_settings()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings_obj.frontend_origin],
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "error_code": exc.error_code})


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error.", "error_code": "INTERNAL_ERROR"})


@app.get("/api/health")
@limiter.exempt
def health():
    db_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        logger.warning("Health check: database unreachable.")

    status_code = 200 if db_ok else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ok" if db_ok else "degraded",
            "service": "action-engine-api",
            "checks": {"database": "ok" if db_ok else "unreachable"},
        },
    )


app.include_router(auth.router)
app.include_router(content.router)
app.include_router(jobs.router)
app.include_router(tasks.router)
app.include_router(settings.router)
app.include_router(webhooks.router)

from app.services import webhook_delivery  # noqa: F401, E402
