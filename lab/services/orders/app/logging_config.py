import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Formats each log record as a single JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "orders",
            "message": record.getMessage(),
        }
        # Extra fields passed with: logger.info("...", extra={"context": {...}})
        context = getattr(record, "context", None)
        if context:
            log.update(context)
        # If an exception occurred, include the traceback
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log)


def setup_logging() -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logger = logging.getLogger("orders")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger