import logging

from predis.sync_runner.runner import run_server_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        print("Rolling up Predis ")
        logger.info("...🥳")
        run_server_async()
    except Exception as error:
        raise Exception("Server Failed to Start")
