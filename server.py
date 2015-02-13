import socket


def server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(10)
    print "listening..."
    try:
        while True:
            conn, addr = server_socket.accept()
            buffsize = 32
            msg = ""
            complete = False
            while not complete:
                line = conn.recv(buffsize)
                if len(line) < buffsize:
                    complete = True
                msg = "{}{}".format(msg, line)
            conn.sendall("You sent: {}".format(msg))
            print "You received: {}".format(msg)
            conn.close()
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == '__main__':
    server()
