import logging
import sys


def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s — %(message)s",
        stream=sys.stderr,
    )
    return logging.getLogger("mcp-doc")
