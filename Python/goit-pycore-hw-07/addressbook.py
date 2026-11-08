from collections import UserDict
from record import Record
from datetime import datetime

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming = []
        today = datetime.today()
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                # Обчислюємо день народження у поточному році
                bday_this_year = bday.replace(year=today.year)
                # Якщо день народження вже пройшов, беремо наступний рік
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                days_until = (bday_this_year - today).days
                if 0 <= days_until <= 7:
                    upcoming.append((record.name.value, record.show_birthday(), days_until))
        return upcoming
