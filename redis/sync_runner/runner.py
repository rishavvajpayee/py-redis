import logging 
import socket
from conf.config import Environment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_server_sync():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (str(Environment.HOST), int(Environment.PORT))
    logger.info(f"Server running on {Environment.HOST}:{Environment.PORT}")
    sock.bind(address)
    sock.listen(1)

    connected_client: int = 0
    while True:
        logger.info("Waiting for connection")
        connection, client_address = sock.accept()

        try:
            logger.info(f"connection from {client_address}")
            connected_client+=1

            msg = f"hey welcome ! connected clients - {connected_client}"
            connection.send(msg.encode())
            conn = True
            while conn:
                data = connection.recv(32)
                if data:
                    if data.decode() == "nuke":
                        conn = False
                    else:
                        connection.send(b'>>' + data)
                else:
                    connection.send(b"no data recieved")
                    break
        except Exception as error:
            raise Exception(f"Socket Failed : {error}")
        finally:
            connection.close()
