from addressbook import AddressBook, Record, save_data, load_data

def main():
    book = load_data()

    while True:
        command = input(">>> ").strip().lower()

        if command == "add":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            rec = Record(name, phone)
            book.add_record(rec)

        elif command == "show":
            print(book)

        elif command == "exit":
            save_data(book)
            print("Address book saved. Goodbye!")
            break

        else:
            print("Unknown command. Use: add, show, exit")

if __name__ == "__main__":
    main()
