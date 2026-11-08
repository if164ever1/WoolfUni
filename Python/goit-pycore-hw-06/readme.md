# 📒 Address Book - Python OOP Project

## 🧠 Overview

This project is a part of the **GoIT Python Core Course (Homework 9)** and demonstrates the use of **Object-Oriented Programming (OOP)** in Python to build a simple yet extendable **Address Book system**. The core functionality is built around managing contact information with support for **adding**, **editing**, **deleting**, and **searching** contacts.

The main purpose of this project is to practice building classes and working with class instances.

---

## 📦 Project Structure
goit-pycore-hw-06/ │ ├── address_book.py 
                     └── README.md


---

## 🛠️ Features

### ✅ Core Classes:

- **Field**  
  A base class for all fields used in contact records.

- **Name**  
  Inherits from `Field`. Represents the contact's name (required).

- **Phone**  
  Inherits from `Field`. Stores phone numbers. Includes **validation** (only 10-digit numbers allowed).

- **Record**  
  Stores a single contact's name and multiple phone numbers. Supports:
  - Adding a phone
  - Removing a phone
  - Editing a phone
  - Searching for a phone

- **AddressBook**  
  Inherits from `UserDict`. Manages all contact records. Supports:
  - Adding a record
  - Searching a record by name
  - Deleting a record

---

## 🚀 How to Run

Make sure you have **Python 3.x** installed.

Run the following command in your terminal:

```bash
python address_book.py

You will see sample operations including adding and editing contacts printed in the console.
Contact name: John, phones: 1234567890; 5555555555
Contact name: Jane, phones: 9876543210
Contact name: John, phones: 1112223333; 5555555555
John: 5555555555

📌 Key Concepts Covered
Object-Oriented Design
Class Inheritance
Data Validation
Composition (using objects inside other classes)
Working with UserDict for custom dictionary-like behavior

❗ Phone Number Validation
Only 10-digit numeric strings are accepted as valid phone numbers. Any other format will raise ValueError.