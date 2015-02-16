from client import client


def test_response_ok():
    msg = "GET /path/to/myindex.html HTTP/1.1\r\nHost: localhost:50000\r\n"
    result = "HTTP/1.1 200 OK\r\n"
    con_type = "Content-Type: text/plain\r\n"
    body = "Content length: {}".format(21)
    # Length of message from file name to end of line
    result = "{}{}{}".format(result, con_type, body)
    assert client(msg) == result


def test_response_post():
    msg = "POST /path/to/myindex.html HTTP/1.1\r\nHost: localhost:50000\r\n"
    result = "HTTP/1.1 405 ERROR\r\n"
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR 405, POST METHOD NOT ALLOWED\r\n"
    result = "{}{}{}".format(result, con_type, body)
    assert client(msg) == result


def test_response_not_supported():
    msg = "GET /path/to/myindex.html HTTP/1.0\r\nHost: localhost:50000\r\n"
    result = "HTTP/1.1 505 ERROR\r\n"
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR 505, HTTP/1.0 NOT SUPPORTED\r\n"
    result = "{}{}{}".format(result, con_type, body)
    assert client(msg) == result


def test_bad_response():
    msg = "This"
    result = "HTTP/1.1 400 ERROR\r\n"
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR 400, BAD REQUEST\r\n"
    result = "{}{}{}".format(result, con_type, body)
    assert client(msg) == result
