"""

    Test Utils
    ~~~~~~~~~~

"""
from biometrics_client._utils import format_error_message


def test_format_error_message() -> None:
    class GoodDummyRequest:
        json = lambda: dict(message="Error")
        text = str(json())

    class BadDummyRequest:
        json = lambda: dict(other_key="some string here")
        text = str(json())

    assert format_error_message(GoodDummyRequest) == "Error"
    assert format_error_message(BadDummyRequest) == "{'other_key': 'some string here'}"
