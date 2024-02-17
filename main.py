"""
Entry point of application
"""

import sys
import logging

from predis.sync_runner.runner import run_server_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        print("Rolling up Predis ")
        logger.info("...🥳")
        run_server_async(args)
    except Exception as error:
        raise Exception(f"Server Failed to Start - {error}")
