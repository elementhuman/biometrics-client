"""

    API Client
    ----------

"""
import requests
from biometrics_client import __version__
from biometrics_client.exceptions import (
    BiometricsApiError,
    BiometricsApiRequestError,
    BiometricsApiInternalError,
    BiometricsApiResultsNotReadyError,
)
from biometrics_client._utils import (
    create_multipart_encoder,
    format_error_message,
    not_ready_signal,
    task_waiter,
)
from pathlib import Path
from urllib.parse import urljoin
from requests.models import Response
from typing import Any, Dict, List, Union, Tuple, Optional, cast


_DEFAULT_HEADERS = {"User-Agent": f"Biometrics-Client v{__version__}"}


class ElementHumanBiometrics:
    """Client for the Element Human Biometrics API.

    Args:
        access_key (str): an access key for the API.
        secret_key (str): a secret key for the API.
        timeout (int): the maximum amount of time to wait for a
            response from the server in seconds.
        url (str): the URL for the API
        verbose (bool): if True print additional information.

    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        timeout: int = 30,
        url: str = "https://biometrics.elementapis.com/public/v0.1/",
        verbose: bool = True,
    ) -> None:
        if not isinstance(url, str) or not url:
            raise TypeError("`url` must be a non-null string.")
        elif not isinstance(access_key, str):
            raise TypeError(f"`access_key` not of type str, got {access_key}.")
        elif not isinstance(secret_key, str):
            raise TypeError(f"`secret_key` not of type str, got {secret_key}.")
        self._access_key = access_key
        self._secret_key = secret_key

        self.timeout = timeout
        self.url = url
        self.verbose = verbose

    @property
    def _credentials(self) -> Dict[str, str]:
        """API Credentials"""
        return {"x-access-key": self._access_key, "x-secret-key": self._secret_key}

    def _print(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    @staticmethod
    def _response_validator(r: Response) -> None:
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException:
            msg = (
                f"Bad response from biometrics api, "
                f"got message: {format_error_message(r).rstrip('.')}."
            )
            if 400 <= r.status_code < 500:
                raise BiometricsApiRequestError(msg)
            elif 500 <= r.status_code < 600:
                raise BiometricsApiInternalError(msg)
            else:
                raise BiometricsApiError(msg)

    def ping(self, **kwargs: Any) -> Dict[str, str]:
        """Ping the API.

        Args:
            **kwargs (Keyword Args): Keyword arguments to pass to
            ``requests``.

        Returns:
            dict

        """
        r = requests.get(urljoin(self.url, "ping"), **kwargs)
        self._response_validator(r)
        return cast(dict, r.json())

    def apply(
        self,
        video_file_path: Path,
        metadata_file_path: Optional[Path] = None,
        analyses: Union[str, List[str], Tuple[str, ...]] = ("emotion",),
        **kwargs: Any,
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """Send a video to the Biometrics API for analysis

        Args:
            video_file_path (Path): a system path to a video
            metadata_file_path (Path, optional): a path to a metadata file.
            analyses (str, list, tuple): analyses to perform on the video.

                * if a string, must be 'all'
                * if a list of strings or a tuple of strings
                    defining analyses to perform. These can be any of
                    the following:

                      * 'face': Face bound box.
                      * 'eye': Eye bounding boxes. Depends on: 'face'.
                      * 'emotion': compute Ekman emotions for the video,
                                   along with quality metrics. Depends on: 'face'.
                      * 'gaze': eye gaze. Depends on: 'face', 'eye'.

            **kwargs (Keyword Args): Keyword arguments to pass to
                ``requests``.

        Returns:
            response (dict)

        """
        multipart_data = create_multipart_encoder(
            video_file_path, metadata_file_path=metadata_file_path
        )
        r = requests.post(
            urljoin(self.url, "apply"),
            data=multipart_data,
            timeout=self.timeout,
            params=dict(analyses=analyses),
            headers={
                "Content-Type": multipart_data.content_type,
                **self._credentials,
                **_DEFAULT_HEADERS,
            },
            **kwargs,
        )
        self._response_validator(r)
        return cast(dict, r.json())

    def results(
        self,
        task_id: str,
        check_interval: int = 10,
        max_wait: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Get a task from the Biometrics API.

        Args:
            task_id (str): a task ID obtained from the /apply endpoint
            check_interval (int): time to wait between checks to determine
                if results are ready. Only applies if ``max_wait`` is not ``None``.
            max_wait (int, optional): the maximum amount of time to wait
                for the results in seconds.
            **kwargs (Keyword Args): Keyword arguments to pass to
                ``requests``.

        Returns:
            response (dict)

        Raises:
            BiometricsApiResultsNotReadyError: if results are not yet ready.

        """

        def fetch() -> Dict[str, Any]:
            r = requests.get(
                urljoin(self.url, f"results/{task_id}"),
                timeout=self.timeout,
                headers={**self._credentials, **_DEFAULT_HEADERS},
                **kwargs,
            )
            if not_ready_signal(r):
                raise BiometricsApiResultsNotReadyError(format_error_message(r))
            self._response_validator(r)
            return cast(dict, r.json())

        output = task_waiter(
            func=fetch,
            max_wait=max_wait,
            sleep_time=check_interval,
            handled_exceptions=(BiometricsApiResultsNotReadyError,),
            timeout_exception=requests.exceptions.ConnectTimeout(
                f"Timed out waiting for task '{task_id}'"
            ),
        )
        return cast(dict, output)

    def apply_and_wait(
        self,
        video_file_path: Path,
        metadata_file_path: Optional[Path] = None,
        analyses: Union[str, List[str], Tuple[str, ...]] = ("emotion",),
        max_wait: Optional[int] = 60 * 30,
        **kwargs: Any,
    ) -> Tuple[str, Dict[str, Any]]:
        """Send a video to the Biometrics API for analysis
        and wait for the results.

        Args:
            video_file_path (Path): a system path to a video
            metadata_file_path (Path, optional): a path to a metadata file.
            analyses (str, list, tuple): analyses to perform on the video.

                * if a string, must be 'all'
                * if a list of strings or a tuple of strings
                    defining analyses to perform. These can be any of
                    the following:

                      * 'face': Face bound box.
                      * 'eye': Eye bounding boxes. Depends on: 'face'.
                      * 'emotion': compute Ekman emotions for the video,
                                   along with quality metrics. Depends on: 'face'.
                      * 'gaze': eye gaze. Depends on: 'face', 'eye'.

            max_wait (int, optional): the maximum amount of time to wait
                for the results in seconds.
            **kwargs (Keyword Args): Keyword arguments to pass to
                ``requests``.

        Returns:
            tuple:
                task_id (str): the task id
                response (dict): the response payload.

        Raises:
            BiometricsApiResultsNotReadyError: if results are not yet ready.

        """
        task = self.apply(
            video_file_path=video_file_path,
            metadata_file_path=metadata_file_path,
            analyses=analyses,
            **kwargs,
        )
        task_id = task["response"]["task_id"]  # type: ignore
        self._print(f"Upload Complete. Task ID: {task_id}.")
        return task_id, self.results(task_id, max_wait=max_wait, **kwargs)
