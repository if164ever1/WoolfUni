from datetime import datetime
import re
from colorama import Fore, Style, init


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\+?\d{10,15}$', value):
            raise ValueError(f"{Fore.RED}Invalid phone number format{Style.RESET_ALL}")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError(f"{Fore.RED}Invalid date format. Use DD.MM.YYYY{Style.RESET_ALL}")
        super().__init__(self.value)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Email(Field):
    def __init__(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError(f"{Fore.RED}Invalid email format{Style.RESET_ALL}")
        super().__init__(value)


class Address(Field):
    pass
