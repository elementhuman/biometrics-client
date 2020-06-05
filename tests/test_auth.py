"""

    Test Auth
    ~~~~~~~~~

"""
import pytest
from biometrics_client import auth


def test_auth1_type_error() -> None:
    with pytest.raises(TypeError):
        auth.Auth1(access_key=99, secret_key="99")


def test_auth2_type_error() -> None:
    with pytest.raises(TypeError):
        auth.Auth2(token=999)


def test_auth1_credentials() -> None:
    creds = dict(access_key="apples", secret_key="cats")
    auth.Auth1(**creds).credentials == creds


def test_auth2_credentials() -> None:
    creds = dict(token="999")
    auth.Auth2(**creds).credentials == creds
