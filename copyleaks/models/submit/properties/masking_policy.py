from enum import IntEnum


class MaskingPolicy(IntEnum):
    NoMask = 0
    MaskOtherUsersFiles = 1
    MaskAllFiles = 2
