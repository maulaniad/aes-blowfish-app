from enum import Enum


class TransactionStatus(Enum):
    ENCRYPTED = "ENCRYPTED"
    DECRYPTED = "DECRYPTED"
    PENDING   = "PENDING"
    FAILURE   = "FAILURE"


class RecentActivityType(Enum):
    ENCRYPTION     = "File Dienkripsi"
    DECRYPTION     = "File Didekripsi"
    FILE_DELETE    = "File Dihapus"
    ACCOUNT_UPDATE = "Akun Diperbarui"
