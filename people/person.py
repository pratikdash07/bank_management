
class Person:
    #Base class representing a person in the bank system.
    def __init__(self, name, phone=None, email=None, address=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    def get_basic_details(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }
