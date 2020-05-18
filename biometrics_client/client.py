"""

    Client
    ~~~~~~

"""
import requests
from biometrics_client.auth import BiometricsAuth
from biometrics_client.exceptions import ResultsNotReady
from biometrics_client._utils import (
    task_waiter,
    create_multipart_encoder,
    not_ready_signal,
)
from pathlib import Path
from urllib.parse import urljoin
from requests.models import Response
from typing import Any, Dict, List, Union, Tuple, Optional


class ElementHumanBiometrics:
    """Client for the Element Human Biometrics API.

    Args:
        auth (BiometricsAuth): api authorization.
        timeout (int): the maximum amount of time to wait for a
            response from the server in seconds.
        url (str): the URL for the API
        verbose (bool): if True print additional information.
        **kwargs (Keyword Args): Keyword arguments to pass to
            ``requests``.

    Notes:
        * Authorization (``auth``) type depends on the ``url``
          being used. If unsure which form of authorization to use,
          use ``Auth1``.

    Examples:
        >>> from pathlib import Path
        >>> from biometrics_client import Auth1, ElementHumanBiometrics
        ...
        >>> biometrics = ElementHumanBiometrics(
        ...    auth=Auth1(
        ...         access_key="YOUR-ACCESS-KEY-HERE",
        ...         secret_key="YOUR-SECRET-KEY-HERE"
        ...     )
        ... )
        ...
        >>> response = biometrics.apply_and_wait(
        ...     video_file_path=Path("path/to/video/file.mp4"),
        ...     analyses=["emotion"],
        ... )

    """

    def __init__(
        self,
        auth: BiometricsAuth,
        timeout: int = 30,
        url: str = "https://biometrics.elementapis.com/public/v0.1/",
        verbose: bool = True,
        **kwargs: Any
    ) -> None:
        self.auth = auth
        self.timeout = timeout
        self.url = url
        self._verbose = verbose
        self._kwargs = kwargs

    @property
    def credentials(self) -> Dict[str, str]:
        """API Credentials"""
        return self.auth.credentials

    def _print(self, msg: str) -> None:
        if self._verbose:
            print(msg)

    def _response_validator(self, r: Response) -> None:
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as error:
            self._print(r.text)
            raise error

    def ping(self) -> Dict[str, str]:
        """Ping the API.

        Returns:
            dict

        """
        r = requests.get(urljoin(self.url, "ping"), **self._kwargs)
        self._response_validator(r)
        return r.json()

    def apply(
        self,
        video_file_path: Path,
        metadata_file_path: Optional[Path] = None,
        analyses: Union[str, List[str], Tuple[str, ...]] = ("emotion",),
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """Send a video to the Biometrics API for analysis

        Args:
            video_file_path (Path): a system path to a video
            metadata_file_path (Path, optional): a path to a metadata file.
            analyses (str, list, tuple): analyses to perform on the video.

                Options:

                    * if a string, must be 'all'

                    * if a list of strings or a tuple of strings
                        defining analyses to perform. These can be any of
                        the following:

                            * 'face': Face bound box.
                            * 'eyes': Eye bounding boxes. Depends on: 'face'.
                            * 'emotion': compute Ekman emotions for the video,
                                    along with quality metrics. Depends on: 'face'.
                            * 'gaze': eye gaze Depends on: 'face', 'eyes'.

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
            headers={"Content-Type": multipart_data.content_type, **self.credentials},
            **self._kwargs
        )
        self._response_validator(r)
        return r.json()

    def results(
        self, task_id: str, check_interval: int = 10, max_wait: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get a task from the Biometrics API.

        Args:
            task_id (str): a task ID obtained from the /apply endpoint
            check_interval (int): time to wait between checks to determine
                if results are ready. Only applies if ``max_wait`` is not ``None``.
            max_wait (int, optional): the maximum amount of time to wait
                for the results in seconds.

        Returns:
            response (dict)

        Warnings:
            * a response with a status code of 400 will be
              returned if the results are not yet ready.

        Raises:
            * ``ResultsNotReady`` is results are not yet ready.

        """

        def fetch() -> Dict[str, Any]:
            r = requests.get(
                urljoin(self.url, f"results/{task_id}"),
                timeout=self.timeout,
                headers=self.credentials,
                **self._kwargs
            )
            if not_ready_signal(r):
                raise ResultsNotReady(r.text)
            self._response_validator(r)
            return r.json()

        return task_waiter(
            func=fetch,
            max_wait=max_wait,
            sleep_time=check_interval,
            handled_exceptions=(ResultsNotReady,),
            timeout_exception=requests.ConnectTimeout(
                f"Timed out waiting for task '{task_id}'"
            ),
        )

    def apply_and_wait(
        self,
        video_file_path: Path,
        metadata_file_path: Optional[Path] = None,
        analyses: Union[str, List[str], Tuple[str, ...]] = ("emotion",),
        max_wait: Optional[int] = 60 * 30,
    ) -> Tuple[str, Dict[str, Any]]:
        """Send a video to the Biometrics API for analysis
        and wait for the results.

        Args:
            video_file_path (Path): a system path to a video
            metadata_file_path (Path, optional): a path to a metadata file.
            analyses (str, list, tuple): analyses to perform on the video.

                Options:

                    * if a string, must be 'all'

                    * if a list of strings or a tuple of strings
                        defining analyses to perform. These can be any of
                        the following:

                            * 'face': Face bound box.
                            * 'eyes': Eye bounding boxes. Depends on: 'face'.
                            * 'emotion': compute Ekman emotions for the video,
                                    along with quality metrics. Depends on: 'face'.
                            * 'gaze': eye gaze Depends on: 'face', 'eyes'.

            max_wait (int, optional): the maximum amount of time to wait
                for the results in seconds.

        Returns:
            tuple:
                task_id (str): the task id
                response (dict): the response payload.

        Raises:
            * ``ResultsNotReady`` is results are not yet ready.

        """
        task = self.apply(
            video_file_path=video_file_path,
            metadata_file_path=metadata_file_path,
            analyses=analyses,
        )
        task_id = task["response"]["task_id"]
        self._print(f"Upload Complete. Task ID: {task_id}.")
        return task_id, self.results(task_id, max_wait=max_wait)
