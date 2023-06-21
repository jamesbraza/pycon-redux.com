from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    DELIVERED = "delivered"
    PLANNED = "planned"
    OTHER = "other"


@dataclass
class Talk:
    status: Status
    date: datetime


today = datetime.now()


def get_display_brute_conditionals(talk: Talk) -> str | None:
    if talk.status == Status.PLANNED:
        if talk.date > today:
            return "future"
        else:
            return "cancelled"
    elif talk.status == Status.DELIVERED:
        if talk.date > today:
            return "rescheduled"
        else:
            return "past"
    return None


def get_display_condensed_conditionals(talk: Talk) -> str | None:
    if talk.status == Status.PLANNED:
        return "future" if talk.date > today else "cancelled"
    elif talk.status == Status.DELIVERED:
        return "rescheduled" if talk.date > today else "past"
    return None


def get_display_lookup(talk: Talk) -> str | None:
    displays = {
        (Status.PLANNED, True): "future",
        (Status.PLANNED, False): "cancelled",
        (Status.DELIVERED, True): "rescheduled",
        (Status.DELIVERED, False): "past",
    }
    return displays.get((talk.status, talk.date > today), None)


def get_display_match(talk: Talk) -> str | None:
    match talk.status, talk.date > today:
        case Status.PLANNED, True:
            return "future"
        case Status.PLANNED, False:
            return "cancelled"
        case Status.DELIVERED, True:
            return "rescheduled"
        case Status.DELIVERED, False:
            return "past"
        case _:
            return None
