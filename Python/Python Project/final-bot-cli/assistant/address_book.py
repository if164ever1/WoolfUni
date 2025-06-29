from collections import UserDict
from datetime import datetime
from assistant.record import Record

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name:str):
        return self.data.get(name)

    def delete(self, name:str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")
        
    def get_upcoming_birthdays(self, days=7):
        upcoming = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)

                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                delta_days = (next_birthday - today).days
                print(f"{record.name.value}: birthday on {next_birthday}, in {delta_days} days")

                if delta_days <= days:
                    upcoming.append(record)

        return upcoming

    
    def search(self, keyword: str):
        results = []
        keyword_lower = keyword.lower()
        for record in self.data.values():
            if keyword_lower in record.name.value.lower():
                results.append(record)
        return results




# Команди для роботи з адресною книгою
# @input_error
# def add_contact(args, book: AddressBook):
#     pass


# @input_error
# def change_phone(args, book: AddressBook):
#     pass


# @input_error
# def show_phones(args, book: AddressBook):
#     pass


# @input_error
# def show_all(book: AddressBook):
#     pass


# @input_error
# def add_birthday(args, book: AddressBook):
#     pass


# @input_error
# def birthdays(args, book: AddressBook):
#     pass