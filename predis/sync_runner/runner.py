"""
Syncronus process Runner with IO multiplexing
"""

import logging
import selectors
import socket
from conf.config import Environment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

total_connections = [0]


def accept(sock: socket.socket, sel: selectors.DefaultSelector, total_connections):
    """
    tasks :
    1. I/O non blocking event for accepting connections
    """
    logger.info(f"Waiting for connection |  curr : {total_connections}")
    connection, client_address = sock.accept()
    total_connections[0] += 1
    connection.setblocking(False)
    connection.send(
        f"welcome {client_address}, total_conn : {total_connections[0]}\n".encode()
    )
    sel.register(connection, selectors.EVENT_READ, read_and_write)


def read_and_write(conn: socket.socket, sel: selectors.BaseSelector, total_connections):
    """
    tasks :
    I/O Non blocking event for reading and writing buffers over the connection
    """
    data = conn.recv(1000)
    if data:
        conn.send(f"~ ".encode() + data)  # Hope this is Non-Blocking
    else:
        sel.unregister(conn)
        conn.close()
        total_connections[0] -= 1


def run_server_async():
    """
    Running Predis

    (main entry point to the application)

    tasks :
    1. creating a selector -> DefaultSelector
    2. new socket
    3. setting the conf of socket to be Non blocking
    4. registering the acceptance of Connections
    """
    sel = selectors.DefaultSelector()
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
