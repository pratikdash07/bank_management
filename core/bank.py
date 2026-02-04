from people.customer import Customer
from people.admin import Admin

from accounts.savings_account import SavingsAccount
from accounts.current_account import CurrentAccount
from accounts.loan_account import LoanAccount


class Bank:    #Central controller/Orchest for the Bank Management System.
    

    def __init__(self):
        self.customers = {}   # customer_id -> Customer object
        self.accounts = {}    # account_number -> Account object
        self.admin = None     # Admin object

    #Admin Setup
    def set_admin(self, admin_id, name, pin):
        self.admin = Admin(admin_id, name, pin)

    def authenticate_admin(self, admin_id, pin):
        if self.admin and self.admin.admin_id == admin_id:
            return self.admin.verify_admin_pin(pin)
        return False

    #Customer Management
    def add_customer(self, customer_id, name, pin, phone=None, email=None, address=None, dob=None, aadhaar_id=None, pan_number=None):
        if customer_id in self.customers:
            raise Exception("Customer already exists")
# Customer Creation
        customer = Customer(
            customer_id=customer_id,
            name=name,
            pin=pin,
            phone=phone,
            email=email,
            address=address,
            dob=dob,
            aadhaar_id=aadhaar_id,
            pan_number=pan_number
        )

        self.customers[customer_id] = customer
        return customer

    def authenticate_customer(self, customer_id, pin):
        customer = self.customers.get(customer_id)
        if not customer:
            return None

        if customer.verify_pin(pin):
            return customer
        return None

    # Account Management 
    def create_account(
        self, account_type,
        account_number,customer_id,
        initial_balance=0.0,
        **kwargs
    ):
        if customer_id not in self.customers:
            raise Exception("Customer does not exist")

        if account_number in self.accounts:
            raise Exception("Account already exists")

        if account_type == "Savings":
            account = SavingsAccount(
                account_number,
                customer_id,
                balance=initial_balance,
                interest_rate=kwargs.get("interest_rate", 0.04),
                minimum_balance=kwargs.get("minimum_balance", 1000)
            )

        elif account_type == "Current":
            account = CurrentAccount(
                account_number,
                customer_id,
                balance=initial_balance,
                overdraft_limit=kwargs.get("overdraft_limit", 5000)
            )

        elif account_type == "Loan":
            account = LoanAccount(
                account_number,
                customer_id,
                loan_amount=kwargs.get("loan_amount"),
                interest_rate=kwargs.get("interest_rate", 0.08)
            )

        else:
            raise ValueError("Invalid account type")

        self.accounts[account_number] = account
        self.customers[customer_id].add_account(account_number)

        return account

    # Cutomer details and info Retrieval
    def get_customer_accounts(self, customer_id):
        customer = self.customers.get(customer_id)
        if not customer:
            return []

        return [
            self.accounts[acc_no]
            for acc_no in customer.get_accounts()
        ]

    def get_account(self, account_number):
        return self.accounts.get(account_number)
