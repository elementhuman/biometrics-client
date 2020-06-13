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
    assert auth.Auth1(**creds).credentials == {
        "x-access-key": creds["access_key"],
        "x-secret-key": creds["secret_key"],
    }


def test_auth2_credentials() -> None:
    authorization = "999"
    assert auth.Auth2(authorization).credentials == dict(authorization=authorization)
