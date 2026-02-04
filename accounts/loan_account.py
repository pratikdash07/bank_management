from accounts.account import Account

class LoanAccount(Account):  # Loan account where balance is negative(Amount owed to bank) and EMI payments are made
    def __init__(
        self,
        account_number,
        customer_id,
        loan_amount,
        interest_rate=0.08
    ):
        super().__init__(account_number, customer_id, balance=-loan_amount)
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        raise Exception("Withdrawals are not allowed for loan accounts")

    def repay_emi(self, amount):
        if amount <= 0:
            raise ValueError("Repayment amount must be positive")

        self._Account__balance += amount
        self._add_transaction("EMI_PAYMENT", amount)

    def calculate_interest(self):
        outstanding = abs(self.get_balance())
        interest = outstanding * self.interest_rate
        self._Account__balance -= interest  ## Name mangling to access private variable(__balance ) --> Advanced OOP topic
        self._add_transaction("INTEREST", interest)
        return interest

    def account_type(self):
        return "Loan"
