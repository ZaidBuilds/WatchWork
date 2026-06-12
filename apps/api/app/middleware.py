import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logging_config import generate_request_id

logger = logging.getLogger("action_engine.middleware")


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", generate_request_id())

        start = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 1)

        response.headers["X-Request-ID"] = request_id
        logger.info(
            "[%s] %s %s -> %s (%sms)",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
