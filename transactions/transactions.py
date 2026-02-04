# transactions/transaction.py

from utils.helpers import get_current_timestamp


class Transaction:
    """
    Represents a single bank transaction.
    """

    def __init__(self, txn_type, amount, balance_after):
        self.transaction_id = self._generate_transaction_id()
        self.type = txn_type
        self.amount = amount
        self.date = get_current_timestamp()
        self.balance_after = balance_after

    def _generate_transaction_id(self):
        return "T" + get_current_timestamp().replace("-", "").replace(":", "").replace(" ", "")

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "type": self.type,
            "amount": self.amount,
            "date": self.date,
            "balance_after": self.balance_after
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.transaction_id = data.get("transaction_id")
        obj.type = data.get("type")
        obj.amount = data.get("amount")
        obj.date = data.get("date")
        obj.balance_after = data.get("balance_after")
        return obj

    def __str__(self):
        return f"{self.date} | {self.type} | {self.amount} | Balance: {self.balance_after}"
