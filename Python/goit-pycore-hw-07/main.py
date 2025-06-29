from addressbook import AddressBook
from handlers import add_contact, change_contact, phone_contact, show_all, add_birthday, show_birthday, upcoming_birthdays

def parse_input(user_input):
    parts = user_input.split()
    command = parts[0]
    args = parts[1:]
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            continue
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone_contact(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(upcoming_birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
