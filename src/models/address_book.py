import re
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self._validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()

class Email(Field):
    def __init__(self, value):
        if not self._validate_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    def _validate_email(self, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, value) is not None

class Address(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            phone_obj.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found in this record.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_date):
        self.birthday = Birthday(birthday_date)

    def add_email(self, email_address):
        self.email = Email(email_address)

    def add_address(self, address_text):
        self.address = Address(address_text)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        email_str = f", email: {self.email.value}" if self.email else ""
        address_str = f", address: {self.address.value}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}{email_str}{address_str}"


class AddressBook(UserDict):    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find_contacts(self, query: str):
        result = []
        query = query.lower()
        
        for record in self.data.values():
            if query in record.name.value.lower():
                result.append(record)
                continue
                
            for phone in record.phones:
                if query in phone.value:
                    result.append(record)
                    break
                    
        return result

    def get_birthdays_per_range(self, days: int):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
                
            birthday_date = record.birthday.date
            
            try:
                birthday_this_year = birthday_date.replace(year=today.year)
            except ValueError:
                birthday_this_year = birthday_date.replace(year=today.year, month=3, day=1)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_delta = (birthday_this_year - today).days

            if 0 <= days_delta <= days:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays