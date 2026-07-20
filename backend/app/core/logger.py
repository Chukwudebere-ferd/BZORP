import logging
import sys


def setup_logging() -> None:
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)
