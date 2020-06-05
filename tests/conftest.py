"""

    Conftest
    ~~~~~~~~

"""
import pytest
from biometrics_client import Auth1, ElementHumanBiometrics


@pytest.fixture()
def dummy_ehb_client() -> ElementHumanBiometrics:
    return ElementHumanBiometrics(Auth1("a", "b"))
