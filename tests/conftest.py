"""

    Conftest
    ~~~~~~~~

"""
import pytest
from tests import DUMMY_ACCESS_KEY, DUMMY_SECRET_KEY
from biometrics_client import ElementHumanBiometrics


@pytest.fixture()
def dummy_ehb_client() -> ElementHumanBiometrics:
    return ElementHumanBiometrics(
        access_key=DUMMY_ACCESS_KEY, secret_key=DUMMY_SECRET_KEY
    )
