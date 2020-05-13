"""

    Utils
    ~~~~~

"""
import io
import time
from pathlib import Path
from os.path import basename
from requests import Response
from requests_toolbelt import MultipartEncoder
from typing import Any, Callable, Type, Union, Tuple, Optional, Dict


def _open_as_bytes(path: Path) -> io.BytesIO:
    with path.open("rb") as f:
        return io.BytesIO(f.read())


def _get_file_type(path: Path) -> str:
    return path.suffix.lstrip(".")


def task_waiter(
    func: Callable[..., Any],
    max_wait: Optional[int],
    sleep_time: int,
    handled_exceptions: Optional[Tuple[Type[BaseException], ...]] = None,
    timeout_exception: Optional[BaseException] = None,
) -> Any:
    """Wait for ``func`` to sucessfully return.

    Args:
        func (callable): a function to run
        max_wait (int, optional): the maximum amount of time to
            wait for ``func`` to sucessfully return.
        sleep_time (int): the amount of time to sleep between
            executions of ``func``
        handled_exceptions (tuple, optional): one or
            more exceptions to handle
        timeout_exception (BaseException, optional): an
            exception to raise if ``max_wait`` is reached.

    Returns:
        Any

    """
    if max_wait is None:
        return func()

    start_time = time.time()
    while (time.time() - start_time) < max_wait:
        try:
            return func()
        except handled_exceptions or tuple():
            time.sleep(sleep_time)
    else:
        if timeout_exception is not None:
            raise timeout_exception
        return None


def not_ready_signal(r: Response) -> bool:
    """Return or not ``r`` is ready.

    Args:
        r (Response): response object.

    Returns:
        bool

    """
    return r.status_code == 400 and "not ready" in r.text.lower()


def add_multipart_data(
    video_file_path: Path, metadata_file_path: Optional[Path] = None
) -> MultipartEncoder:
    """Create a multipart encoder

    Args:
        video_file_path (Path): a system path to a video
        metadata_file_path (Path, optional): a path to a metadata file.

    Returns:
        MultipartEncoder

    """

    def make_value(path: Path) -> Dict[str, Union[bytes, str]]:
        return (
            basename(str(path)),
            _open_as_bytes(path),
            f"video/{_get_file_type(path)}",
        )

    fields = dict(video_file=make_value(video_file_path))
    if metadata_file_path:
        fields["metadata"] = make_value(metadata_file_path)
    return MultipartEncoder(fields)
