def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args

def add_contact(args, contacts):
    if len(args) < 2:
        return "Невірний формат. Використовуйте: add [ім'я] [номер]"
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    if len(args) < 2:
        return "Невірний формат. Використовуйте: change [ім'я] [новий номер]"
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    return "Contact not found."

def show_phone(args, contacts):
    if len(args) < 1:
        return "Невірний формат. Використовуйте: phone [ім'я]"
    name = args[0]
    return contacts.get(name, "Contact not found.")

def show_all(contacts):
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()]) if contacts else "No contacts found."

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()