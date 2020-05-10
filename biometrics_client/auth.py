"""

    Authorization
    ~~~~~~~~~~~~~

"""
from typing import Any, Dict


def _credentials_type_checker(credentials: Dict[str, str]) -> None:
    for k, v in credentials.items():
        if not isinstance(k, str):
            raise TypeError(f"Expected key of type str, got {k}.")
        if not isinstance(v, str):
            raise TypeError(f"Expected value of type str, got {v}.")


class BiometricsAuth:
    """Biometrics authorization base class.

    Args:
        **credentials (Keyword Args): keyword arguments
            for API authorization.

    """

    def __init__(self, **credentials) -> None:
        _credentials_type_checker(credentials)
        self.credentials = credentials


class Auth1(BiometricsAuth):
    """First form of Biometrics API authorization.

    Args:
        access_key (str): an access key for the API
        secret_key (str): a secret key for the API
    """

    def __init__(self, access_key: str, secret_key: str) -> None:
        super().__init__(**{"x-access-key": access_key, "x-secret-key": secret_key})


class Auth2(BiometricsAuth):
    """Second form of Biometrics API authorization.

    Args:
        authorization (str): an access token.

    """

    def __init__(self, authorization: str) -> None:
        super().__init__(authorization=authorization)
