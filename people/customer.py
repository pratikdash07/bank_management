from people.person import Person

class Customer(Person):# Represents a bank customer.
    
    def __init__(
        self,
        customer_id,
        name,
        pin,
        phone=None,
        email=None,
        address=None,
        dob=None,
        aadhaar_id=None,
        pan_number=None
    ):
        super().__init__(name, phone, email, address)

        self.customer_id = customer_id
        self.__pin = str(pin)          # private for security
        self.accounts = []             # list of account numbers
        self.dob = dob                  # Optional details
        self.aadhaar_id = aadhaar_id
        self.pan_number = pan_number

    #Authentication/Secutiry
    def verify_pin(self, pin):
        return self.__pin == str(pin)

    def change_pin(self, old_pin, new_pin):
        if self.verify_pin(old_pin):
            self.__pin = str(new_pin)
            return True
        return False

    #Account Management 
    def add_account(self, account_number):
        if account_number not in self.accounts:
            self.accounts.append(account_number)

    def get_accounts(self):
        return self.accounts

    #Admin-level visibility (controlled) #for admin use only.
    def _get_pin_for_admin(self):
        return self.__pin
