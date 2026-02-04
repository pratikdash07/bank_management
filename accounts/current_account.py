from accounts.account import Account

class CurrentAccount(Account): # Curr acc with overdraft facility(Basically Credit)
    def __init__(
        self,
        account_number,
        customer_id,
        balance=0.0,
        overdraft_limit=5000
    ):
        super().__init__(account_number, customer_id, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if self.get_balance() - amount < -self.overdraft_limit:
            raise Exception("Overdraft limit exceeded")

        self._Account__balance -= amount
        self._add_transaction("WITHDRAW", amount)

    def calculate_interest(self):
        return 0.0

    def account_type(self):
        return "Current"
