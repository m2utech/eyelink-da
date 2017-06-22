import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("m2u-da.eastus.cloudapp.azure.com", 5225))
    data = ""
    sock.sendall(data)
    result = sock.recv(1024)
    print(result)
    sock.close()