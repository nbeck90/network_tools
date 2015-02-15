from client import client
import pytest


def test_response_ok():
    msg = "GET /path/to/myindex.html HTTP/1.1\r\nHost: localhost:50000\r\n"
    result = "HTTP/1.1 200 OK\r\n"
    con_type = "Content-Type: text/plain\r\n"
    body = "Content length: {}".format(21)
    # Length of message from file name to end of line
    result = "{}{}{}".format(result, con_type, body)
    assert client(msg) == result
