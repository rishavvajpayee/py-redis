"""
Entry point of application
"""

import sys
import logging

from predis.runner import run_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        print("Rolling up Predis ")
        logger.info("...🥳")
        run_server(args)
    except Exception as error:
        raise Exception(f"Server Failed to Start - {error}")
