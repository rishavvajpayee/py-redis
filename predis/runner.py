"""
Syncronus process Runner with IO multiplexing
"""

import os
import logging
import selectors
import socket
from conf.config import Environment
from .resolver import (
    resolve_ping,
    resolve_get,
    resolve_set,
)
from conf.enums import Methods

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

total_connections = [0]

def unregister_close(sel: selectors.BaseSelector, conn: socket.socket):
    sel.unregister(conn)
    conn.close()


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


def get_method(request: str):
    if " " in request:
        return request.split(" ")[0]
    else:
        return request.split("\n")[0]


def read_and_write(conn: socket.socket, sel: selectors.BaseSelector, total_connections: list[int]):
    """
    tasks :
    I/O Non blocking event for reading and writing buffers over the connection
    """
    data = conn.recv(1024)
    if data:
        request = data.decode()
        method = get_method(request)
        resolve = ""
        nuked = False
        match method:
            case Methods.SET:
                resolve = resolve_set(request)
            case Methods.GET:
                resolve = resolve_get(request)
            case Methods.PING:
                resolve = resolve_ping()
            case Methods.NUKE:
                unregister_close(sel, conn)
                total_connections[0] -= 1
                logger.info("connection was closed")
                nuked = True
            case Methods.NUKEBANG:
                unregister_close(sel, conn)
                logger.critical("connection was force closed")
                total_connections = [0]
                nuked = True
                os._exit(45)
            case _:
                resolve = request
        if not nuked:
            conn.send(b"~ " + resolve.encode() + b"\r\n")  # Hope this is Non-Blocking
    else:
        sel.unregister(conn)
        conn.close()
        total_connections[0] -= 1


def run_server(args: None | list):
    """
    Running Predis
    (main entry point to the application)

    tasks :
    1. creating a selector -> DefaultSelector
    2. new socket
    3. setting the conf of socket to be Non blocking
    4. registering the acceptance of Connections
    """
    HOST = None
    PORT = None
    if args:
        if "-p" in args:
            PORT_INDEX = args.index("-p") + 1
            try:
                PORT = int(args[PORT_INDEX])
            except TypeError as error:
                raise TypeError(f"incompatible type for PORT : {error}")
        if "-h" in args:
            HOST_INDEX = args.index("-h") + 1
            try:
                HOST = str(args[HOST_INDEX])
            except TypeError as error:
                raise TypeError(f"incompatible type for HOST : {error}")

    sel = selectors.DefaultSelector()
    sock = socket.socket()
    sock.bind(
        (
            str(Environment.HOST) if not HOST else HOST,
            int(Environment.PORT) if not PORT else PORT,
        )
    )

    logger.info(f"Binding HOST : http://{HOST}:{PORT}")
    sock.listen(100)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj, sel, total_connections)
