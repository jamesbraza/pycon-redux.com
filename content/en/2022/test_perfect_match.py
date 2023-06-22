from collections.abc import Callable

import pytest
from datetime import timedelta
from perfect_match import (
    get_display_brute_conditionals,
    Talk,
    Status,
    get_display_condensed_conditionals,
    get_display_lookup,
    get_display_match,
    today,
)

FUTURE = today + timedelta(days=1)
PAST = today + timedelta(days=-1)


@pytest.mark.parametrize(
    "func",
    [
        get_display_brute_conditionals,
        get_display_condensed_conditionals,
        get_display_lookup,
        get_display_match,
    ],
)
@pytest.mark.parametrize(
    ("talk", "expected"),
    [
        (Talk(Status.PLANNED, FUTURE), "future"),
        (Talk(Status.PLANNED, PAST), "cancelled"),
        (Talk(Status.DELIVERED, FUTURE), "rescheduled"),
        (Talk(Status.DELIVERED, PAST), "past"),
        (Talk(Status.OTHER, FUTURE), None),
        (Talk(Status.OTHER, PAST), None),
    ],
)
def test_get_display_variants(
    func: Callable[[Talk], str | None], talk: Talk, expected: str | None
) -> None:
    assert func(talk) == expected
