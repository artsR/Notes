

class AddressBookEntry(object):
    version = 0.1

    """ '__init__'  is a CONSTRUCTOR. It will be called automatically
    when a new INSTANCE (object) will be created"""
    def __init__(self, name, phone):
        self.name  = name
        self.phone = phone

    def update_phone(self, phone):
        self.phone = phone
