"""

    Conftest
    ~~~~~~~~

"""
import pytest
from biometrics_client import ElementHumanBiometrics


@pytest.fixture()
def dummy_ehb_client() -> ElementHumanBiometrics:
    return ElementHumanBiometrics(access_key="a", secret_key="b")
