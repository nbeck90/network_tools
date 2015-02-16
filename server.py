import socket
import os
import io
import mimetypes
import email.utils


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


def response_ok(msg, resolved):
    result = "\nHTTP/1.1 200 OK\r\n"
    timestamp = 'Date: {}\r\n'.format(email.utils.formatdate(usegmt=True))
    con_type = "Content-Type: {}".format(msg)
    body = "{}".format(resolved)
    return "{}{}{}{}".format(result, timestamp, con_type, body)


def response_error(error_code, error_msg):
    error_type = "HTTP/1.1 {} ERROR\r\n".format(error_code)
    timestamp = 'Date: {}\r\n'.format(email.utils.formatdate(usegmt=True))
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR {}, {}\r\n".format(error_code, error_msg)
    return "{}{}{}{}".format(error_type, timestamp, con_type, body)


def parse_request(request):
    request_pieces = request.split()
    if len(request_pieces) != 5:
        return None
    error_check = check_errors(request_pieces)
    if error_check == 'No Errors':
        resolved = resolve_uri(request_pieces[1])
        return resolved
    return error_check


def check_errors(request):
    if request[0] != 'GET':
        return response_error('405', '{} METHOD NOT ALLOWED'.format(request[0]))
    if request[2] != 'HTTP/1.1':
        return response_error('505', '{} NOT SUPPORTED'.format(request[2]))
    return 'No Errors'


def resolve_uri(uri):
    if os.path.isfile(uri):
        file_content = read_file(uri)
        guess = mimetypes.guess_type(uri)[0]
        response = response_ok(guess, file_content)
        return response
    elif os.path.isdir(os.path.abspath(uri)):
        files = file_list(uri)
        response = response_ok('text/html', files)
        return response
    else:
        return response_error('404', 'Content Not Found')


def read_file(uri):
    file_info = io.open(uri, "r")
    body = file_info.read()
    file_info.close()
    return body


def file_list(uri):
    file_list = ""
    for item in os.listdir(uri):
        file_list += "<li>{}</li>\n".format(item)
    body = "\n\n<ul>\n{}</ul>\n".format(file_list)
    return body


if __name__ == '__main__':
    server()
