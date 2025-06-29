from assistant.address_book import AddressBook
from assistant.notesbook import NotesBook
from assistant.serialization import save_data, load_data
from assistant.parser import parse_command, execute_command
from colorama import Fore, Style, init

init(autoreset=True)


try:
    contacts, notes = load_data()
except Exception as e:
    print(Fore.RED + f"Error loading data: {e}")
    contacts = AddressBook()
    notes = NotesBook()


def print_help():
    print(Fore.YELLOW + Style.BRIGHT + "\n💡 Available Commands:\n")
    print(Fore.CYAN + "📇 Contact Management:")
    print("  ➕ add contact <name> <phone>")
    print("  📞 edit phone <name> <old_phone> <new_phone>")
    print("  🗑️ delete contact <name>")
    print("  🔍 find contact <keyword>")
    print("  📋 show contacts\n")

    print(Fore.MAGENTA + "🎂 Birthday Management:")
    print("  🎁 add birthday <name> <DD.MM.YYYY>")
    print("  📆 edit birthday <name> <DD.MM.YYYY>")
    print("  🔮 birthday <days>\n")

    print(Fore.BLUE + "📧 Email & Address:")
    print("  📧 add/edit email <name> <email>")
    print("  🏠 add/edit address <name> <address>\n")

    print(Fore.GREEN + "🗒️ Notes:")
    print("  ✍️ add note <text>")
    print("  🔍 note find <tag>")
    print("  🔃 note sort !")
    print("  🗑️ note delete <text>\n")

    print(Fore.RED + "🚪 Exit:")
    print("  ❌ exit | quit | close\n" + Style.RESET_ALL)


def main():
    print(Fore.GREEN + "👋 Welcome to your Personal Assistant CLI!")
    print_help()
    while True:
        user_input = input(Fore.CYAN + ">>> " + Style.RESET_ALL)
        if user_input.lower() in ['exit', 'quit', 'close']:
            save_data(contacts, notes)
            print(Fore.GREEN + "👋 Bye! All data saved.")
            break

        command, arguments = parse_command(user_input)
        try:
            execute_command(command, arguments, contacts, notes)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")


if __name__ == "__main__":
    main()
