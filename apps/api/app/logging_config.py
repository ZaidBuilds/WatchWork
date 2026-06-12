import json
import logging
import sys
import uuid
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        request_id = getattr(record, "request_id", None)
        if request_id:
            log_entry["request_id"] = request_id
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging(log_level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root.handlers = [handler]

    for noisy in ("httpcore", "httpx", "uvicorn.access"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def generate_request_id() -> str:
    return uuid.uuid4().hex[:12]
