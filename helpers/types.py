from typing import TypedDict

from helpers.enums import RecentActivityType


ARCHIVES = (
    "zip",
    "rar",
    "7z",
    "tar",
    "tar.gz",
    "tar.bz2",
    "tar.xz",
    "tar.lzma",
    "tar.zst",
    "tar.Z",
    "tgz",
    "tbz2"
)


ICONS = {
    RecentActivityType.ENCRYPTION: "bx bxs-lock",
    RecentActivityType.DECRYPTION: "bx bx-lock-open",
    RecentActivityType.FILE_DELETE: "bx bx-trash",
    RecentActivityType.ACCOUNT_UPDATE: "bx bxs-user"
}


COLORS = {
    RecentActivityType.ENCRYPTION: "text-sky-500",
    RecentActivityType.DECRYPTION: "text-orange-500",
    RecentActivityType.FILE_DELETE: "text-red-500",
    RecentActivityType.ACCOUNT_UPDATE: "text-blue-500"
}


class RecentActivityDict(TypedDict):
    action: str
    box_icon: str
    user: str
    time_difference: str
