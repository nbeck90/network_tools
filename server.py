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
            complete = False
            print "You received: "
            while not complete:
                line = conn.recv(buffsize)
                if len(line) < buffsize:
                    complete = True
                message = line
                out = message
                print out
            conn.sendall(out)
    except KeyboardInterrupt:
        conn.close()
        server_socket.close()


if __name__ == '__main__':
    server()
