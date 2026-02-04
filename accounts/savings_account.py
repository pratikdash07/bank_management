from accounts.account import Account  #classes implement the blueprint(Account)

class SavingsAccount(Account):
    def __init__(
        self,
        account_number,
        customer_id,
        balance=0.0,
        interest_rate=0.04, # 4% interest rate
        minimum_balance=1000 
    ):
        super().__init__(account_number, customer_id, balance)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if self.get_balance() - amount < self.minimum_balance:
            raise Exception("Minimum balance requirement not met")

        super().withdraw(amount)

    def calculate_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        return interest

    def account_type(self):
        return "Savings"