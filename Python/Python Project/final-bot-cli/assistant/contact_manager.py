from datetime import datetime
from colorama import Fore, Style, init
import re

init(autoreset=True)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        pattern = r'^\d{10}$'
        if not re.match(pattern, value):
            raise ValueError(
                f"{Fore.RED}Invalid phone number format{Style.RESET_ALL}")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(
                f"{Fore.RED}Invalid date format. Use DD.MM.YYYY{Style.RESET_ALL}")
        super().__init__(parsed_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
