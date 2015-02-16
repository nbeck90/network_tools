from client import client
import email.utils


def test_response_not_found():
    msg = "GET /path/to/myindex.html HTTP/1.1\r\nHost: localhost:50000\r\n"
    result = "\nHTTP/1.1 404 ERROR\r\n"
    date = 'Date: {}\r\n'.format(email.utils.formatdate(usegmt=True))
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR 404, Content Not Found\r\n"
    # Length of message from file name to end of line
    result = "{}{}{}{}".format(result, date, con_type, body)
    assert client(msg) == result


def test_response_post():
    msg = "POST /path/to/myindex.html HTTP/1.1\r\nHost: localhost:50000\r\n"
    result = "\nHTTP/1.1 405 ERROR\r\n"
    date = 'Date: {}\r\n'.format(email.utils.formatdate(usegmt=True))
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR 405, POST METHOD NOT ALLOWED\r\n"
    result = "{}{}{}{}".format(result, date, con_type, body)
    assert client(msg) == result


def test_response_not_supported():
    msg = "GET /path/to/myindex.html HTTP/1.0\r\nHost: localhost:50000\r\n"
    result = "\nHTTP/1.1 505 ERROR\r\n"
    date = 'Date: {}\r\n'.format(email.utils.formatdate(usegmt=True))
    con_type = "Content-Type: text/plain\r\n"
    body = "ERROR 505, HTTP/1.0 NOT SUPPORTED\r\n"
    result = "{}{}{}{}".format(result, date, con_type, body)
    assert client(msg) == result


def test_dir_response():
    msg = "GET webroot/ HTTP/1.1\r\nHost: localhost:50001\r\n"
    assert "<li>make_time.py</li>" in client(msg)
    # Ensure display of files
    assert "<li>images</li>" in client(msg)
    # Ensure display of directory


def test_file_response():
    msg = "GET webroot/make_time.py HTTP/1.1\r\nHost: localhost:50001\r\n"
    assert "simple script that returns and HTML page with the current time"\
        in client(msg)
