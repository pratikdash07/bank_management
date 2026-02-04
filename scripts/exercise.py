import os
import sys

# Ensure project root is on sys.path when running this script from /scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.datastore import DataStore
from utils.helpers import generate_customer_id, generate_account_number, generate_pin


def unique_customer_id(bank):
    cid = generate_customer_id()
    while cid in bank.customers:
        cid = generate_customer_id()
    return cid


def unique_account_no(bank):
    acc = generate_account_number()
    while acc in bank.accounts:
        acc = generate_account_number()
    return acc


def run_exercise():
    ds = DataStore()
    bank = ds.load_bank()

    print("Customers before:", len(bank.customers))

    # 1) Add new customer
    cid = unique_customer_id(bank)
    pin = generate_pin()
    cust = bank.add_customer(customer_id=cid, name="Test User", pin=pin)
    print("Added customer:", cid, cust.name)

    # 2) Create a Savings account for the new customer
    acc_no = unique_account_no(bank)
    account = bank.create_account("Savings", acc_no, cid, initial_balance=5000)
    print("Created account:", acc_no, "Type:", account.account_type(), "Balance:", account.get_balance())

    # 3) Deposit and Withdraw
    account.deposit(1500)
    print("After deposit, balance:", account.get_balance())

    try:
        account.withdraw(2000)
        print("After withdrawal, balance:", account.get_balance())
    except Exception as e:
        print("Withdrawal error:", e)

    # 4) Create a Current account and test overdraft
    acc2 = unique_account_no(bank)
    current = bank.create_account("Current", acc2, cid, initial_balance=100)
    print("Created current account:", acc2, "Balance:", current.get_balance())
    try:
        current.withdraw(1000)  # within overdraft if limit allows
        print("Current after overdraft withdrawal, balance:", current.get_balance())
    except Exception as e:
        print("Overdraft withdrawal error:", e)

    # 5) Create a Loan account and make EMI repayment
    loan_acc_no = unique_account_no(bank)
    loan = bank.create_account("Loan", loan_acc_no, cid, loan_amount=10000)
    print("Created loan account:", loan_acc_no, "Balance (negative):", loan.get_balance())
    loan.repay_emi(2000)
    print("After EMI payment, loan balance:", loan.get_balance())

    # 6) Inspect transactions for savings account
    print("Transactions for savings account:")
    for t in account.transactions:
        print(" -", t)

    # 7) Close one account
    account.close()
    print("Closed account:", account.account_number, "Status:", account.status)

    # 8) Persist changes
    ds.save_bank(bank)
    print("Saved bank state. Customers now:", len(bank.customers))


if __name__ == "__main__":
    run_exercise()
