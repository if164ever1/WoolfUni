from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if isinstance(value, str) and value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    def delete(self, name):
        if name in self.data:
            del self.data[name]

if __name__ == "__main__":
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    for name, record in book.data.items():
        print(record)
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")
    book.delete("Jane")
