from fields import Name, Phone, Birthday

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return None

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday = self.show_birthday() or "N/A"
        return f"Record(Name: {self.name.value}, Phones: {phones}, Birthday: {birthday})"
