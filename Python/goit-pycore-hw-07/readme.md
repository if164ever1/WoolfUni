# 📒 Assistant Bot - Advanced OOP in Python

## 🧠 Overview

This project is an advanced object-oriented programming project in Python that extends our previous homeworks by implementing an **address book assistant bot**. The bot allows you to manage contacts, including phone numbers and birthdays, and provides useful commands for interaction.

## 📦 Project Structure
goit-pycore-hw-07/ │ ├── fields.py # Contains Field, Name, Phone, and Birthday classes. 
                     ├── record.py # Contains the Record class with methods for managing phones birthdays. 
                     ├── addressbook.py # Contains the AddressBook class, a custom dictionary for storing contacts. 
                     ├── decorators.py # Contains the @input_error decorator for error handling. 
                     ├── handlers.py # Contains command handler functions (add_contact, change_contact, etc.). 
                     ├── main.py # Main bot interface that parses commands and interacts with the AddressBook. 
                     └── README.md # Project documentation.


## 🚀 Features

- **Contact Management**: Add new contacts or update existing ones.
- **Phone Number Handling**: Validate that phone numbers consist of exactly 10 digits.
- **Birthday Management**:
  - Add a birthday to a contact (format: `DD.MM.YYYY`).
  - Show a contact's birthday.
  - List upcoming birthdays within the next week.
- **Command Interface**:  
  The bot supports the following commands:
  - `add [name] [phone]`
  - `change [name] [old_phone] [new_phone]`
  - `phone [name]`
  - `all`
  - `add-birthday [name] [birthday in DD.MM.YYYY]`
  - `show-birthday [name]`
  - `birthdays`
  - `hello`
  - `close` or `exit`
- **Error Handling**:  
  Uses the `@input_error` decorator to catch input errors and display friendly error messages.
- **Data Validation**:
  - Phone numbers must be 10 digits.
  - Birthdays must follow the format `DD.MM.YYYY`.

## 🛠️ How to Run

1. **Clone the repository:**
   ```bash
   git clone <repository_url>

Navigate to the project directory:
cd goit-pycore-hw-07

Run the bot:
python main.py

Welcome to the assistant bot!
Enter a command: add John 1234567890
Contact added.
Enter a command: add-birthday John 15.04.1990
Birthday added.
Enter a command: show-birthday John
John's birthday: 15.04.1990
Enter a command: birthdays
John: 15.04.1990 (in 5 days)
Enter a command: exit
Good bye!


📌 Notes
The Birthday field converts the input string into a datetime object for further processing.

The method get_upcoming_birthdays in the AddressBook class returns contacts whose birthdays occur within the next 7 days.

All input errors and exceptions are caught by the @input_error decorator, ensuring robust user interaction.