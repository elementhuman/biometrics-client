"""

    Exceptions
    ~~~~~~~~~~

"""


class BiometricsClientError(Exception):
    pass


class ResultsNotReady(BiometricsClientError):
    pass
