# Personal Assistant CLI (final-bot-cli)

A command-line based personal assistant that helps you manage contacts and notes. Designed for structured organization, this assistant supports searching, editing, tagging, and birthday reminders — all from your terminal.

---

## 📌 Features

### 🧑‍🤝‍🧑 Contact Management
- Add, edit, delete contacts
- Store multiple phone numbers per contact
- Add birthdays with automatic upcoming birthday reminders
- Validate phone numbers and birthdates

### 📝 Notes Management
- Create, edit, delete text notes
- Tag notes with keywords
- Search notes by tag
- Sort notes by tag
- Store notes persistently

### 💾 Data Storage
- Automatically saves contacts and notes using `pickle`
- Data persists between program restarts
- Stored in local `/data` folder as `.bin` file

### 💻 CLI Interface
- Intuitive command parser
- Supports commands like: `add contact`, `add note`, `edit note`, `delete contact`, `note find tag`, etc.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Install dependencies:
```bash
pip install -r requirements.txt

python -m cli.main



ADD
add contact John +380991112233
add birthday John 25.12.1995
add email John john@example.com
add address John Kyiv, Ukraine
show contacts

Contact name: John, phones: +380991112233, birthday: 25.12.1995, email: john@example.com, address: Kyiv, Ukraine

FIND
add contact John +380991112233
add contact Joanna +380671234567
add contact Mike +380931112233
find contact jo

DELETE
delete contact John

EDIT
edit phone John +380991112233 +380999999999
edit birthday John 01.01.2000
edit email John new_email@example.com
edit address John Lviv, Ukraine
edit address John Lviv, Ukraine

UPCOMING BIRTHDAY
add contact Mike +380931112233
add birthday Mike <дата через 5 днів>  ← підстави актуальну дату
birthday 5

NOTES
add note Learn Python
add note Buy milk
note find learn    
note find milk      
note find something 