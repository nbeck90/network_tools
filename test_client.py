from client import client
import pytest


def test_string_input():
    assert client("String") == "You sent: String"


def test_int_input():
    assert client(42) == "You sent: 42"


def test_empty_input():
    with pytest.raises(TypeError):
        client()


def test_over32_input():
    assert client("A long message that will be over 32 bits but here's a few more")\
    == "You sent: A long message that will be over 32 bits but here's a few more"
