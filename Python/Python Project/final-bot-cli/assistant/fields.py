from datetime import datetime
import re
from colorama import Fore, Style, init


# Клас для базового поля (Field) і його наслідування
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
            raise ValueError("Invalid phone number format") + Fore.RED
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Email(Field):
    def __init__(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        super().__init__(value)

class Address(Field):
    pass 
