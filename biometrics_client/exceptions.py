"""

    Package Exceptions
    ------------------

"""


class BiometricsClientError(Exception):
    """Base biometrics client error"""

    pass


class BiometricsApiError(BiometricsClientError):
    """Generic biometrics api request error."""

    pass


class BiometricsApiRequestError(BiometricsClientError):
    """Generic biometrics api error."""

    pass


class BiometricsApiResultsNotReadyError(BiometricsClientError):
    """Results not ready error."""

    pass


class BiometricsApiInternalError(BiometricsClientError):
    """Internal Biometrics API Error."""

    pass
