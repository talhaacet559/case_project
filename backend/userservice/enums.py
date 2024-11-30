from enum import Enum


class IzinStatus(Enum):
    INITIATED = "INITIATED"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)
