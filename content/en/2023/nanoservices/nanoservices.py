import contextlib
import itertools
from collections import deque
from collections.abc import Generator, Iterable
from typing import Any


class DumpData(Exception):
    """Exception used to indicate the window's contents should be dumped."""


class ClearWindow(Exception):
    """Exception used to indicate the window should be cleared."""


def moving_window_average_gen(
    data: Iterable[float] = (),
    window_size: int = 3,
) -> Generator[float | int | None, float, None]:
    """Run a nanoservice for a simple moving window average.

    Starter: https://docs.python.org/3/library/collections.html#deque-recipes

    Args:
        data: Data to pre-fill into the deque, to avoid bias from little data.
        window_size: Window size for the moving window average.

    Returns:
        Generator that intakes a new value and returns an average.
    """
    window = deque(data, maxlen=window_size)
    current_sum = sum(window)

    def on_new_value(value: Any) -> float:
        if not isinstance(value, int | float):
            raise TypeError(f"Please send in numbers, not {type(value)}.")
        nonlocal current_sum
        current_sum += value if len(window) < window_size else value - window.popleft()
        window.append(value)
        return current_sum / len(window)

    out_value: float | None = None
    while True:
        try:
            print("MWA nanoservice: waiting after yield.")
            in_value = yield out_value
        except DumpData:
            print("MWA nanoservice: providing length.")
            yield len(window)
            print("MWA nanoservice: dumping data.")
            # NOTE: use islice since deque doesn't support slicing
            yield from itertools.islice(window, len(window) - 1)
            out_value = window[-1]  # Trick to avoid extra next call
            continue
        except ClearWindow:
            print("MWA nanoservice: clearing window.")
            window.clear()
            current_sum = 0
            out_value = None
            continue
        except GeneratorExit:
            print("MWA nanoservice: exiting.")
            raise

        try:
            out_value = on_new_value(in_value)
        except TypeError:
            print(f"MWA nanoservice: rejected input {in_value!r}.")
            out_value = None


def demo() -> None:
    mwa_nanoservice = moving_window_average_gen()
    next(mwa_nanoservice)  # Initialize to first yield

    # 1. General usage
    assert mwa_nanoservice.send(5) == 5
    assert mwa_nanoservice.send(7) == 6
    # Check we handle someone forgetting a value or sending wrong type
    assert next(mwa_nanoservice) is None
    assert mwa_nanoservice.send("unexpected") is None  # type: ignore[arg-type]
    assert mwa_nanoservice.send(9) == 7
    assert mwa_nanoservice.send(11) == 9

    # 2. Dumping all data from moving window
    num_datapoints = mwa_nanoservice.throw(DumpData)
    assert tuple(
        next(mwa_nanoservice) for _ in range(num_datapoints)  # type: ignore[arg-type]
    ) == (7, 9, 11)
    assert mwa_nanoservice.send(13) == 11

    # 3. Clearing the window's contents
    assert mwa_nanoservice.throw(ClearWindow) is None
    assert mwa_nanoservice.send(15) == 15

    # 4. Shut down the nanoservice
    mwa_nanoservice.close()
    with contextlib.suppress(StopIteration):
        assert mwa_nanoservice.send(17) is None
