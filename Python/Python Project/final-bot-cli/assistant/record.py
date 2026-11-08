from .fields import Name, Phone, Birthday, Email, Address



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                self.phones.remove(p)
                self.phones.append(Phone(new_phone))
                return
        raise ValueError("Phone number not found.")
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def add_email(self, email):
        self.email = Email(email)
    
    def add_address(self, address):
        self.address = Address(address)
    
    def __str__(self):
        parts = [f"Contact name: {self.name.value}"]
        if self.phones:
            parts.append("phones: " + '; '.join(p.value for p in self.phones))
        if self.birthday:
            parts.append(f"birthday: {self.birthday}")
        if self.email:
            parts.append(f"email: {self.email}")
        if self.address:
            parts.append(f"address: {self.address}")
        return ", ".join(parts)
    
    
    
#NEED TO BE DELETED    
'''
# Клас Record: запис для контакту
class Record:
    pass

    def add_phone(self, phone):
        pass

    def remove_phone(self, phone):
        pass

    def edit_phone(self, old_phone, new_phone):
        pass

    def add_birthday(self, birthday):
        pass

    def days_to_birthday(self):
        pass

    def __str__(self):
        pass
'''