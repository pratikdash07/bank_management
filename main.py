from core.datastore import DataStore
from utils.helpers import generate_account_number

def admin_menu(bank, datastore):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. View all customers")
        print("2. Add new customer")
        print("3. Reset customer PIN")
        print("4. Create new account")
        print("5. View all accounts")
        print("6. Close account")
        print("7. Logout")



        choice = input("Enter choice: ")

        if choice == "1":
            for cid, cust in bank.customers.items():
                print(f"{cid} | {cust.name} | Accounts: {cust.accounts}")

        elif choice == "2":
            cid = input("Customer ID: ")
            name = input("Name: ")
            pin = input("PIN (4 digits): ")

            bank.add_customer(cid, name, pin)
            print("Customer added successfully.")

        elif choice == "3":
            cid = input("Customer ID: ")
            customer = bank.customers.get(cid)

            if not customer:
                print("Customer not found.")
            else:
                new_pin = input("New PIN: ")
                bank.admin.reset_customer_pin(customer, new_pin)
                print("PIN reset successfully.")

        elif choice == "4":
            customer_id = input("Customer ID: ")

            if customer_id not in bank.customers:
                print("Customer not found.")
                continue

            print("Account Types:")
            print("1. Savings")
            print("2. Current")
            print("3. Loan")

            acc_choice = input("Choose account type: ")

            acc_map = {
            "1": "Savings",
            "2": "Current",
            "3": "Loan"
            }

            if acc_choice not in acc_map:
                print("Invalid account type.")
                continue

            account_type = acc_map[acc_choice]
            while True:
                account_number = generate_account_number()
                if account_number not in bank.accounts:
                    break

            if account_type == "Loan":
                loan_amount = float(input("Loan amount: "))
                account = bank.create_account(
                account_type,
                account_number,
                customer_id,
                loan_amount=loan_amount
            )
            else:
                initial_balance = float(input("Initial balance: "))
                account = bank.create_account(
                account_type,
                account_number,
                customer_id,
                initial_balance=initial_balance
                )

            print("\n✅ Account created successfully!")
            print(f"Account Number: {account.account_number}")
            print(f"Account Type  : {account.account_type()}")

        elif choice == "5":
            for acc_no, acc in bank.accounts.items():
                print(
                    f"{acc_no} | {acc.account_type()} | "
                    f"Customer: {acc.customer_id} | "
                    f"Balance: {acc.get_balance()}"
                )
        
        elif choice == "6":
            acc_no = input("Account number to close: ")
            account = bank.accounts.get(acc_no)

            if not account:
                print("Account not found.")
            else:
                account.close()
                datastore.save_bank(bank)
                print(f"Account {acc_no} closed successfully.")

        
        elif choice == "7":
            datastore.save_bank(bank)
            print("Logged out.")
            break

        else:
            print("Invalid choice.")
        



def customer_menu(bank, datastore, customer):
    while True:
        print(f"\n--- CUSTOMER MENU ({customer.name}) ---")
        print("1. View accounts")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View transactions")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            for acc in bank.get_customer_accounts(customer.customer_id):
                print(
                    f"{acc.account_number} | {acc.account_type()} | "
                    f"Balance: {acc.get_balance()}"
                )

        elif choice == "2":
            acc_no = input("Account number: ")
            amount = float(input("Amount to deposit: "))
            account = bank.get_account(acc_no)

            if account and account.customer_id == customer.customer_id:
                account.deposit(amount)
                print("Deposit successful.")
            else:
                print("Invalid account.")

        elif choice == "3":
            acc_no = input("Account number: ")
            amount = float(input("Amount to withdraw: "))
            account = bank.get_account(acc_no)

            if account and account.customer_id == customer.customer_id:
                try:
                    account.withdraw(amount)
                    print("Withdrawal successful.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Invalid account.")

        elif choice == "4":
            for acc in bank.get_customer_accounts(customer.customer_id):
                print(f"\nTransactions for {acc.account_number}:")
                for txn in acc.transactions:
                    print(txn)

        elif choice == "5":
            datastore.save_bank(bank)
            print("Logged out.")
            break

        else:
            print("Invalid choice.")


def main():
    datastore = DataStore()
    datastore.initialize_dummy_data()
    bank = datastore.load_bank()

    while True:
        print("\n====== BANK MANAGEMENT SYSTEM ======")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_id = input("Admin ID: ")
            pin = input("Admin PIN: ")

            if bank.authenticate_admin(admin_id, pin):
                admin_menu(bank, datastore)
            else:
                print("Invalid admin credentials.")

        elif choice == "2":
            cid = input("Customer ID: ")
            pin = input("PIN: ")

            customer = bank.authenticate_customer(cid, pin)
            if customer:
                customer_menu(bank, datastore, customer)
            else:
                print("Invalid customer credentials.")

        elif choice == "3":
            datastore.save_bank(bank)
            print("Thank you for using the system.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
# End of main.py