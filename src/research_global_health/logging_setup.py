import logging
import sys


def setup_logging(level: str) -> None:
    """Configure application logging."""
    root_logger = logging.getLogger()

    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)
    root_logger.setLevel(level.upper())

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
