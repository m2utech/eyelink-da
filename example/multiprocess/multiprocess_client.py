import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9000))
    data = "some data"
    sock.sendall(data)
    result = sock.recv(1024)
    print result
    sock.close()