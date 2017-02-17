import daemon

from elda_main import socket_server

with daemon.DaemonContext():
    socket_server()
