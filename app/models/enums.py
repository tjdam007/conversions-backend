from enum import Enum


class Status(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    CONVERTED = 2
    FAILED = 3


class SizeUnits(Enum):
    BYTES = 0
    KB = 1
    MB = 2
