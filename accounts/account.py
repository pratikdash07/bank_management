
from abc import ABC, abstractmethod
from transactions.transactions import Transaction


class Account(ABC):
    # Abstract base class for all account types.
    def __init__(self, account_number, customer_id, balance=0.0):
        self.account_number = account_number
        self.customer_id = customer_id
        self.__balance = float(balance)   # Prevents fraud or accidents(Pvt variable)
        self.status = "active"             # active / frozen
        self.transactions = []             # list of transaction records

    def deposit(self, amount):
        if self.status != "active":
            raise Exception("Account is not active")

        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.__balance += amount
        self._add_transaction("DEPOSIT", amount)

    def withdraw(self, amount):
        # Child classes may override this method. To carry out basic withdrawal checks.
        
        if self.status != "active":
            raise Exception("Account is not active")

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.__balance:
            raise Exception("Insufficient balance")

        self.__balance -= amount
        self._add_transaction("WITHDRAW", amount)

    def get_balance(self):
        return self.__balance
#Transaction handling
    def _add_transaction(self, txn_type, amount):
        txn = Transaction(txn_type, amount, self.get_balance())
        self.transactions.append(txn)

    #functions to freeze and unfreeze account
    def freeze(self):
        self.status = "frozen"

    def unfreeze(self):
        self.status = "active"

    # ---------- Abstract Methods ----------
    @abstractmethod
    def calculate_interest(self):
        """
        Each account type must define its own interest logic.
        """
        pass

    @abstractmethod
    def account_type(self):
        """
        Returns the account type as string.
        """
        pass
    def close(self):
        self.status = "closed"
