from .record import Record


def parse_command(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    arguments = parts[1:]
    return command, arguments


def execute_command(command: str, arguments: list, book, notes_manager):
    if command == "add":
        if arguments and arguments[0] == "contact":
            if len(arguments) < 3:
                print("❗ Please provide both name and phone.")
                return
            name = arguments[1]
            phone = arguments[2]
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"✅ Contact '{name}' added with phone {phone}")

        elif arguments and arguments[0] == "note":
            text = ' '.join(arguments[1:])
            if not text:
                print("❗ Cannot add empty note.")
                return
            notes_manager.add_note(text)
            print(f"📝 Note added: {text}")

        elif arguments and arguments[0] == "birthday":
            if len(arguments) < 3:
                print("❗ Please provide name and birthday in format DD.MM.YYYY.")
                return
            name = arguments[1]
            birthday = arguments[2]
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            try:
                record.add_birthday(birthday)
                print(f"🎂 Birthday added for {name}: {birthday}")
            except ValueError as e:
                print(f"❗ Error: {e}")

        elif arguments and arguments[0] == "email":
            if len(arguments) < 3:
                print("❗ Please provide name and email.")
                return
            name = arguments[1]
            email = arguments[2]
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            try:
                record.add_email(email)
                print(f"📧 Email added for {name}: {email}")
            except ValueError as e:
                print(f"❗ Error: {e}")

        elif arguments and arguments[0] == "address":
            if len(arguments) < 3:
                print("❗ Please provide name and address.")
                return
            name = arguments[1]
            address = ' '.join(arguments[2:])
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            record.add_address(address)
            print(f"📮 Address added for {name}: {address}")

    elif command == "delete":
        if arguments and arguments[0] == "contact":
            if len(arguments) < 2:
                print("❗ Please provide the contact name to delete.")
                return
            name = arguments[1]
            try:
                book.delete(name)
                print(f"🗑️ Contact '{name}' deleted.")
            except KeyError:
                print(f"❌ Contact '{name}' not found.")

    elif command == "show":
        if arguments and arguments[0] == "contacts":
            if not book.data:
                print("ℹ️ No contacts available.")
                return
            for record in book.data.values():
                print(record)

    elif command == "birthday":
        try:
            days = int(arguments[0]) if arguments else 7
        except ValueError:
            print("❗ Please enter a number of days (e.g., birthday 7)")
            return

        upcoming = book.get_upcoming_birthdays(days)
        if not upcoming:
            print(f"🎉 No upcoming birthdays in the next {days} day(s).")
        else:
            print(f"🎉 Upcoming birthdays in next {days} day(s):")
            for record in upcoming:
                print(f"🎂 {record.name.value} — {record.birthday}")

    elif command == "note":
        if len(arguments) < 2:
            print("❗ Usage: 'note find <tag>' or 'note sort'")
            return

        elif command == "add" and arguments and arguments[0] == "note":
            text = ' '.join(arguments[1:])
            notes_manager.add_note(text)
            print(f"📝 Note added: {text}")

        elif command == "edit" and arguments and arguments[0] == "note":
            if len(arguments) < 3:
                print("❗ Usage: edit note <old_text> <new_text>")
                return
            old_text = arguments[1]
            new_text = ' '.join(arguments[2:])
            success = notes_manager.edit_note(old_text, new_text)
            if success:
                print(f"✏️ Note updated: {new_text}")
            else:
                print("❌ Note not found.")

        elif command == "delete" and arguments and arguments[0] == "note":
            if len(arguments) < 2:
                print("❗ Usage: delete note <text>")
                return
            text = ' '.join(arguments[1:])
            success = notes_manager.delete_note(text)
            if success:
                print(f"🗑️ Note deleted: {text}")
            else:
                print("❌ Note not found.")

        elif command == "note":
            if len(arguments) < 2:
                print("❗ Usage: note find <tag> or note sort")
                return

            if arguments[0] == "find":
                tag = arguments[1]
                notes = notes_manager.find_notes_by_tag(tag)
                if notes:
                    print(f"🔎 Found notes with tag '{tag}':")
                    for note in notes:
                        print(note)
                else:
                    print("🔍 No matching notes found.")

            if arguments[0] == "delete":
                if len(arguments) < 2:
                    print("❗ Usage: delete note <text>")
                    return
                text = ' '.join(arguments[1:])
                success = notes_manager.delete_note(text)
                if success:
                    print(f"🗑️ Note deleted: {text}")
                else:
                    print("❌ Note not found.")

            if arguments[0] == "sort":
                sorted_notes = notes_manager.sort_notes_by_tag()
                if sorted_notes:
                    print("📑 Sorted notes by tag:")
                    for note in sorted_notes:
                        print(note)
                else:
                    print("ℹ️ No notes to sort.")

    elif command == "find":
        if arguments and arguments[0] == "contact":
            if len(arguments) < 2:
                print("❗ Please provide a search keyword.")
                return
            keyword = arguments[1]
            results = book.search(keyword)
            if results:
                print(f"🔍 Found {len(results)} contact(s):")
                for r in results:
                    print(r)
            else:
                print(f"❌ No contacts found with '{keyword}'.")

    elif command == "edit":
        if arguments and arguments[0] == "phone":
            if len(arguments) < 4:
                print("❗ Usage: edit phone <name> <old_phone> <new_phone>")
                return
            name, old_phone, new_phone = arguments[1], arguments[2], arguments[3]
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            try:
                record.edit_phone(old_phone, new_phone)
                print(f"📞 Phone updated for {name}: {old_phone} → {new_phone}")
            except ValueError as e:
                print(f"❗ Error: {e}")

        elif arguments and arguments[0] == "email":
            if len(arguments) < 3:
                print("❗ Usage: edit email <name> <new_email>")
                return
            name, new_email = arguments[1], arguments[2]
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            try:
                record.add_email(new_email)
                print(f"📧 Email updated for {name}: {new_email}")
            except ValueError as e:
                print(f"❗ Error: {e}")

        elif arguments and arguments[0] == "address":
            if len(arguments) < 3:
                print("❗ Usage: edit address <name> <new_address>")
                return
            name = arguments[1]
            new_address = ' '.join(arguments[2:])
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            record.add_address(new_address)
            print(f"📮 Address updated for {name}: {new_address}")

        elif arguments and arguments[0] == "birthday":
            if len(arguments) < 3:
                print("❗ Usage: edit birthday <name> <new_birthday>")
                return
            name, new_birthday = arguments[1], arguments[2]
            record = book.find(name)
            if not record:
                print(f"❌ Contact '{name}' not found.")
                return
            try:
                record.add_birthday(new_birthday)
                print(f"🎂 Birthday updated for {name}: {new_birthday}")
            except ValueError as e:
                print(f"❗ Error: {e}")
