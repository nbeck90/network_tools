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
            buffsize = 16
            msg = ""
            complete = False
            while not complete:
                line = conn.recv(buffsize)
                msg = "{}{}".format(msg, line)
                if len(line) < buffsize:
                    complete = True
            response = parse_request(msg)
            try:
                conn.sendall(response)
            except TypeError:
                conn.sendall(response_error('400', 'BAD REQUEST'))
            conn.close()
    except KeyboardInterrupt:
        print "\nServer successfully shut down"
        server_socket.close()


def response_ok(msg):
    result = "HTTP/1.1 200 OK\r\n"
    con_type = "Content-Type: text/plain\r\n"
    body = "Content length: {}".format(len(msg))
    return "{}{}{}".format(result, con_type, body)


def response_error(error_code, error_msg):
    error_type = "HTTP/1.1 {} ERROR\r\n".format(error_code)
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR {}, {}\r\n".format(error_code, error_msg)
    return "{}{}{}".format(error_type, con_type, body)


def parse_request(request):
    request_pieces = request.split()
    if len(request_pieces) != 5:
        return None
    error_check = check_errors(request_pieces)
    if error_check == 'No Errors':
        return response_ok(request_pieces[1])
    return error_check


def check_errors(request):
    if request[0] != 'GET':
        return response_error('405', '{} METHOD NOT ALLOWED'.format(request[0]))
    if request[2] != 'HTTP/1.1':
        return response_error('505', '{} NOT SUPPORTED'.format(request[2]))
    return 'No Errors'


if __name__ == '__main__':
    server()
