"""

    Client
    ~~~~~~

"""
import io
import requests
import time
from biometrics_client.exceptions import ResultsNotReady
from os.path import basename
from pathlib import Path
from urllib.parse import urljoin
from requests.models import Response
from requests_toolbelt import MultipartEncoder
from typing import Any, Dict, List, Union, Tuple


def _open_as_bytes(path: Path) -> io.BytesIO:
    with path.open("rb") as f:
        return io.BytesIO(f.read())


def _get_file_type(path: Path) -> str:
    return path.suffix.lstrip(".")


def _not_ready(r: Response) -> bool:
    return r.status_code == 400 and "not ready" in r.text.lower()


class ElementHumanBiometrics:
    """Simple tool for interacting with Element Human's Biometrics API

    Args:
        access_key (str): an access key for the API
        secret_key (str): a secret key for the API
        timeout (int): the maximum amount of time to wait for a
            response from the server in seconds.
        url (str): the URL for the API
        verbose (bool): if True print additional information.

    Examples:
        >>> biometrics = ElementHumanBiometrics(
        ...    access_key="YOUR-ACCESS-KEY-HERE",
        ...    secret_key="YOUR-SECRET-KEY-HERE"
        ... )
        >>> result = biometrics.apply_and_wait(
        ...     video_file_path=Path("path/to/video/file.mp4"),
        ...     analyses=["emotion"],
        ... )

    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        timeout: int = 30,
        url: str = "https://biometrics.elementapis.com/public/v0.1/",
        verbose: bool = True,
    ) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.timeout = timeout
        self.url = url
        self._verbose = verbose

        self._sleep_time: int = 10

    @property
    def _credentials(self) -> Dict[str, str]:
        return {"x-access-key": self.access_key, "x-secret-key": self.secret_key}

    def _print(self, msg: str) -> None:
        if self._verbose:
            print(msg)

    def _response_validator(self, r: Response) -> None:
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as error:
            self._print(r.text)
            raise error

    def apply(
        self,
        video_file_path: Path,
        analyses: Union[List[str], Tuple[str, ...]] = ("emotion",),
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """Send a video to the Biometrics API for analysis

        Args:
            video_file_path (Path): a system path to a video
            analyses (list, tuple): a list of strings denoting the
                analyses one would like performed on the video.

                Options:

                    * 'emotions': compute Ekman emotions for the video,
                       along with quality metrics.

        Returns:
            response (dict)

        """
        multipart_data = MultipartEncoder(
            fields={
                "video_file": (
                    basename(str(video_file_path)),
                    _open_as_bytes(video_file_path),
                    f"video/{_get_file_type(video_file_path)}",
                )
            }
        )
        r = requests.post(
            urljoin(self.url, "apply"),
            data=multipart_data,
            timeout=self.timeout,
            params=dict(analyses=list(analyses)),
            headers={"Content-Type": multipart_data.content_type, **self._credentials},
        )
        self._response_validator(r)
        return r.json()

    def results(self, task_id: str) -> Dict[str, Any]:
        """Get a task from the Biometrics API.

        Args:
            task_id (str): a task ID obtained from the /apply endpoint

        Returns:
            response (dict)

        Warnings:
            * a response with a status code of 400 will be
              returned if the results are not yet ready.

        """
        r = requests.get(
            urljoin(self.url, f"results/{task_id}"),
            timeout=self.timeout,
            headers=self._credentials,
        )
        if _not_ready(r):
            raise ResultsNotReady(r.text)
        self._response_validator(r)
        return r.json()

    def apply_and_wait(
        self,
        video_file_path: Path,
        analyses: Union[List[str], Tuple[str, ...]] = ("emotion",),
        max_wait: int = 60 * 30,
    ) -> Dict[str, Any]:
        """Send a video to the Biometrics API for analysis
        and wait for the results.

        Args:
            video_file_path (Path): a system path to a video
            analyses (list, tuple): a list of strings denoting the
                analyses one would like performed on the video.

                Options:

                    * 'emotions': compute Ekman emotions for the video,
                       along with quality metrics.

            max_wait (int): the maximum amount of time to wait for the results
                in seconds.

        Returns:
            response (dict)

        Warnings:
            * a response with a status code of 400 will be
              returned if the results are not yet ready.

        """
        task = self.apply(video_file_path, analyses=analyses)
        task_id = task["response"]["task_id"]
        self._print(f"Upload Complete. Task ID: {task_id}.")

        start_time = time.time()
        while (time.time() - start_time) < max_wait:
            try:
                return self.results(task_id)
            except ResultsNotReady:
                time.sleep(self._sleep_time)
        else:
            raise requests.ConnectTimeout(f"Timed out waiting for task '{task_id}'")
