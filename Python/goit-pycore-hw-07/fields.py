from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if isinstance(value, str) and value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits")

class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(date_obj)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
