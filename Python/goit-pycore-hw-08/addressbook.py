import pickle

class Record:
    def __init__(self, name, phone=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def __str__(self):
        return f"{self.name}: {', '.join(self.phones)}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name] = record

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# --- серіалізація та десеріалізація ---

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
