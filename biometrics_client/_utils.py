"""

    Utils
    ~~~~~

"""
import time
from typing import Any, Callable, Type, Union, Tuple, Optional


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
