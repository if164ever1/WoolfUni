# Project: Python File Handling and CLI Applications

## Overview

This project contains various Python scripts that demonstrate file handling, directory structure visualization, and a simple CLI assistant bot. Below are the details of each script and how to use them.

## Project Structure

```
📦 goit-pycore-hw-04
 ┣ 📂 .git
 ┣ 📂 venv
 ┣ 📜 total_salary.py
 ┣ 📜 salary_file.txt
 ┣ 📜 get_cats_info.py
 ┣ 📜 cats_file.txt
 ┣ 📜 directory_structure.py
 ┣ 📜 assistant_bot.py
 ┗ 📜 README.md
```

## Requirements

Before running the scripts, ensure you have **Python 3.x** installed on your system. Additionally, install the required dependencies using:

```bash
pip install -r requirements.txt
```

Or manually install **colorama** if needed:

```bash
pip install colorama
```

## How to Use Each Script

### 1. `total_salary.py`

This script reads a salary file and calculates the total and average salary.

#### Usage:

```bash
python total_salary.py salary_file.txt
```

### 2. `get_cats_info.py`

Reads a file containing cat information and returns structured data.

#### Usage:

```bash
python get_cats_info.py cats_file.txt
```

### 3. `directory_structure.py`

Displays the directory structure with color-coded output for better visualization.

#### **How to Run `directory_structure.py` Correctly**

To properly execute the script, follow these steps:

1. **Navigate to your project directory**
   Open a terminal (Command Prompt `cmd`, PowerShell, or a terminal in VS Code) and change the directory to your project folder:
   
   ```bash
   cd D:\IT\WOOLF\HW\goit-pycore-hw-04
   ```

2. **(Optional) Activate Virtual Environment**
   If you are using a virtual environment (`venv`), activate it before running the script:

   #### **For Windows (CMD):**
   ```bash
   venv\Scripts\activate
   ```
   
   #### **For Windows (PowerShell):**
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   
   #### **For Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the script**
   Execute the following command to visualize the structure of your project directory:
   
   ```bash
   python directory_structure.py D:\IT\WOOLF\HW\goit-pycore-hw-04
   ```
   
4. **Expected Output**
   The script will display the folder structure in the terminal with:
   - **Directories** in **blue**
   - **Files** in **green**
   
   Example output:
   ```
   picture/
       bot-icon.png
       Logo/
           IBM+Logo.png
           ibm.svg
           logo-tm.png
       mongodb.jpg
   ```

### 4. `assistant_bot.py`

A simple command-line assistant bot for managing contacts.

#### Usage:

```bash
python assistant_bot.py
```

#### Available Commands:

- `hello` → Responds with "How can I help you?"
- `add [name] [phone]` → Adds a contact.
- `change [name] [new_phone]` → Updates a contact.
- `phone [name]` → Shows a contact's phone number.
- `all` → Displays all contacts.
- `exit` / `close` → Exits the bot.

## Running in a Virtual Environment (Recommended)

If you are using a virtual environment (`venv`), activate it before running the scripts:

### **For Windows (CMD):**

```bash
venv\Scripts\activate
```

### **For Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

### **For Mac/Linux:**

```bash
source venv/bin/activate
```

Then, proceed with running the scripts as mentioned above.

## License

This project is for educational purposes and is free to use and modify.

---

For any issues or questions, feel free to contact the author.