from gevent.monkey import patch_all
from gevent.server import StreamServer
from server import parse_request


def new_server(socket, address):
    buffsize = 16
    try:
        msg = ""
        complete = False
        while not complete:
            line = socket.recv(buffsize)
            if line:
                msg += line
            else:
                socket.sendall(parse_request(msg))
                socket.close()
                complete = True
    except KeyboardInterrupt:
        print "\nServer successfully closed\n"
        socket.close()


if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), new_server)
    print "Listening..."
    server.serve_forever()
