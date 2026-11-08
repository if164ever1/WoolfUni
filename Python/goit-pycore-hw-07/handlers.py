from record import Record
from addressbook import AddressBook
from decorators import input_error

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Usage: add [name] [phone]")
    name, phone, *rest = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Usage: change [name] [old_phone] [new_phone]")
    name, old_phone, new_phone, *rest = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def phone_contact(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Usage: phone [name]")
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    phones = ", ".join(p.value for p in record.phones)
    return f"{name}: {phones}"

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    result = ""
    for name, record in book.data.items():
        phones = ", ".join(p.value for p in record.phones)
        birthday = record.show_birthday() or "N/A"
        result += f"{name}: Phones: {phones}, Birthday: {birthday}\n"
    return result.strip()

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Usage: add-birthday [name] [birthday in DD.MM.YYYY]")
    name, birthday_str, *rest = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday_str)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if record is None or record.birthday is None:
        return "Birthday not found for this contact."
    return f"{name}'s birthday: {record.show_birthday()}"

@input_error
def upcoming_birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    result = ""
    for name, birthday, days in upcoming:
        result += f"{name}: {birthday} (in {days} days)\n"
    return result.strip()
