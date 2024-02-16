import logging

from redis.sync_runner.runner import run_server_sync

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        run_server_sync()
    except Exception as error:
        raise Exception("Server Failed to Start")
