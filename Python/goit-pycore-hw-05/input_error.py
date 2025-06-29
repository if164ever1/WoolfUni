def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "This contact does not exist."
        except IndexError:
            return "Give me name and phone please."
        except Exception:
            return "Something went wrong. Please try again."
    return inner

contacts = {}

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def get_phone(args, contacts):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    return contacts[name]

@input_error
def show_all(args, contacts):
    if len(args) != 0:
        raise IndexError
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    while True:
        command = input("Enter a command: ").strip()
        if command == 'add':
            print("Enter the argument for the command")
            args = input().split()
            print(add_contact(args, contacts))
        elif command == 'phone':
            print("Enter the argument for the command")
            args = input().split()
            print(get_phone(args, contacts))
        elif command == 'all':
            print(show_all([], contacts))
        elif command == 'exit':
            print("Goodbye!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
