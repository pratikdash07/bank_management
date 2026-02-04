from people.person import Person

class Admin(Person): # Represents a bank admin. Admin has overide privileges over customer.
    def __init__(self, admin_id, name, admin_pin):
        super().__init__(name)

        self.admin_id = admin_id
        self.__admin_pin = str(admin_pin)

    #Authentication for admin actions
    def verify_admin_pin(self, pin):
        return self.__admin_pin == str(pin)

    #Admin Controls 
    def reset_customer_pin(self, customer, new_pin):
        #Admin has access to change customer PIN directly
        customer._Customer__pin = str(new_pin)

    def view_customer_pin(self, customer):
        #Admin can view customer PIN if needed.
        return customer._get_pin_for_admin()
