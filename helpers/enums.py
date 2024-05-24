from enum import Enum


class TransactionStatus(Enum):
    ENCRYPTED = "ENCRYPTED"
    DECRYPTED = "DECRYPTED"
    PENDING   = "PENDING"
    FAILURE   = "FAILURE"
