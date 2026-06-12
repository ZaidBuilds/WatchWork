import logging

from fastapi import HTTPException, status

logger = logging.getLogger("action_engine")


class AppError(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = ""):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class NotFoundError(AppError):
    def __init__(self, resource: str = "Resource"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource} not found.", error_code="NOT_FOUND")


class UnauthorizedError(AppError):
    def __init__(self, detail: str = "Authentication required."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, error_code="UNAUTHORIZED")


class ForbiddenError(AppError):
    def __init__(self, detail: str = "Not authorized."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, error_code="FORBIDDEN")


class ConflictError(AppError):
    def __init__(self, detail: str = "Resource already exists."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, error_code="CONFLICT")


class ValidationError(AppError):
    def __init__(self, detail: str = "Invalid input."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail, error_code="VALIDATION_ERROR")


class RateLimitError(AppError):
    def __init__(self, detail: str = "Rate limit exceeded."):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail, error_code="RATE_LIMITED")


class ExternalServiceError(AppError):
    def __init__(self, service: str, detail: str = ""):
        msg = f"External service error: {service}" + (f" - {detail}" if detail else "")
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=msg, error_code="EXTERNAL_SERVICE_ERROR")
