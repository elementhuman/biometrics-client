"""

    Exceptions
    ~~~~~~~~~~

"""


class BiometricsClientError(Exception):
    """Base biometrics client error"""

    pass


class BiometricsResultsNotReadyError(BiometricsClientError):
    """Results not ready error."""

    pass
