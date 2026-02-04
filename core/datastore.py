# core/datastore.py

import json
import os
import random

from core.bank import Bank
from utils.helpers import (
    generate_customer_id,
    generate_account_number,
    generate_pin
)
from transactions.transactions import Transaction


class DataStore:
    """
    Handles loading and saving bank data to JSON.
    """

    def __init__(self, file_path="data/bank_data.json"):
        self.file_path = file_path

    # ---------- File Handling ----------
    def _read_file(self):
        if not os.path.exists(self.file_path):
            return {}

        with open(self.file_path, "r") as f:
            return json.load(f) or {}

    def _write_file(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    # ---------- Load Data ----------
    def load_bank(self):
        data = self._read_file()
        bank = Bank()

        # Admin
        admin_data = data.get("admin")
        if admin_data:
            bank.set_admin(
                admin_data["admin_id"],
                admin_data["name"],
                admin_data["pin"]
            )

        # Customers
        for cust_id, cust_data in data.get("customers", {}).items():
            customer = bank.add_customer(
                customer_id=cust_id,
                name=cust_data["name"],
                pin=cust_data["pin"],
                phone=cust_data.get("phone"),
                email=cust_data.get("email"),
                address=cust_data.get("address")
            )
            customer.accounts = cust_data.get("accounts", [])

        # Accounts
        for acc_no, acc_data in data.get("accounts", {}).items():
            acc_type = acc_data["type"]
            extra = acc_data.get("extra", {})

            account = bank.create_account(
                account_type=acc_type,
                account_number=acc_no,
                customer_id=acc_data["customer_id"],
                initial_balance=acc_data["balance"],
                **extra
            )

            account.status = acc_data.get("status", "active")
            account.transactions = [
                Transaction.from_dict(t) if isinstance(t, dict) else t
                for t in acc_data.get("transactions", [])
            ]

        return bank

    # ---------- Save Data ----------
    def save_bank(self, bank):
        data = {
            "admin": {
                "admin_id": bank.admin.admin_id,
                "name": bank.admin.name,
                "pin": bank.admin._Admin__admin_pin
            },
            "customers": {},
            "accounts": {}
        }

        for cust_id, customer in bank.customers.items():
            data["customers"][cust_id] = {
                "name": customer.name,
                "pin": customer._get_pin_for_admin(),
                "phone": customer.phone,
                "email": customer.email,
                "address": customer.address,
                "accounts": customer.accounts
            }

        for acc_no, account in bank.accounts.items():
            data["accounts"][acc_no] = {
                "type": account.account_type(),
                "customer_id": account.customer_id,
                "balance": account.get_balance(),
                "status": account.status,
                "transactions": [
                    t.to_dict() if hasattr(t, "to_dict") else t
                    for t in account.transactions
                ],
                "extra": self._extract_extra_fields(account)
            }

        self._write_file(data)

    # ---------- Dummy Data Initialization ----------
    def initialize_dummy_data(self, count=50):
        if self._read_file():
            return  # Already initialized

        bank = Bank()
        bank.set_admin("ADMIN", "System Owner", 9999)

        for _ in range(count):
            cust_id = generate_customer_id()
            pin = generate_pin()

            customer = bank.add_customer(
                customer_id=cust_id,
                name=f"Customer {cust_id}",
                pin=pin
            )

            for _ in range(random.randint(1, 3)):
                acc_type = random.choice(["Savings", "Current"])
                acc_no = generate_account_number()
                balance = random.randint(1000, 50000)

                bank.create_account(
                    acc_type,
                    acc_no,
                    cust_id,
                    initial_balance=balance
                )

        self.save_bank(bank)

    # ---------- Helpers ----------
    def _extract_extra_fields(self, account):
        if account.account_type() == "Savings":
            return {
                "interest_rate": account.interest_rate,
                "minimum_balance": account.minimum_balance
            }

        if account.account_type() == "Current":
            return {
                "overdraft_limit": account.overdraft_limit
            }

        if account.account_type() == "Loan":
            return {
                "interest_rate": account.interest_rate,
                "loan_amount": account.loan_amount
            }

        return {}
