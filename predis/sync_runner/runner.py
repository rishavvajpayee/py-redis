import logging
import selectors
import socket
from conf.config import Environment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

total_connections = [0]


def accept(sock: socket.socket, sel: selectors.DefaultSelector, total_connections):
    logger.info(f"Waiting for connection |  curr : {total_connections}")
    connection, client_address = sock.accept()
    total_connections[0] += 1
    connection.setblocking(False)
    connection.send(
        f"welcome {client_address}, total_conn : {total_connections[0]}\n".encode()
    )
    sel.register(connection, selectors.EVENT_READ, read_and_write)


def read_and_write(
    connection: socket.socket, sel: selectors.BaseSelector, total_connections
):
    data = connection.recv(1000)
    if data:
        connection.send(f"~ ".encode() + data)  # Hope this is Non-Blocking
    else:
        sel.unregister(connection)
        connection.close()
        total_connections[0] -= 1


def run_server_async():
    sel: selectors.DefaultSelector = selectors.DefaultSelector()
    sock = socket.socket()
    sock.bind((str(Environment.HOST), int(Environment.PORT)))
    sock.listen(100)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj, sel, total_connections)
