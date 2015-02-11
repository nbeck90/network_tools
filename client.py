import sys
import socket


space = " "
message = space.join(sys.argv[1:])


def client(msg):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(message)
    client_socket.shutdown(socket.SHUT_WR)
    buffsize = 32
    response = ""
    complete = False
    while not complete:
        line = client_socket.recv(buffsize)
        if len(line) < buffsize:
            complete = True
        response = "{}{}".format(response, line)
    client_socket.close()


if __name__ == '__main__':
    client(message)
