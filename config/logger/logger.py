import sys

from loguru import logger


logger.add(
    sys.stderr,
    level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | [{level}] | {message}"
)
