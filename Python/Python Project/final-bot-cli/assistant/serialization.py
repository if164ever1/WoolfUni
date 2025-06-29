from colorama import init, Fore
import pickle
from collections import UserDict
from datetime import datetime, timedelta
from assistant.address_book import AddressBook

init(autoreset=True)

def save_data(book, notes_manager, filename="addressbook.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump((book, notes_manager), f)
        print(f"{Fore.GREEN}Data successfully saved to {filename}.")  
    except Exception as e:
        print(f"{Fore.RED}Error saving data: {e}") 

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            book, notes_manager = pickle.load(f)
        print(f"{Fore.GREEN}Data successfully loaded from {filename}.") 
        return book, notes_manager
    except FileNotFoundError:
        print(f"{Fore.YELLOW}File {filename} not found. A new address book will be created.")  
        return AddressBook()
    except Exception as e:
        print(f"{Fore.RED}Error loading data: {e}")  
        return AddressBook()
