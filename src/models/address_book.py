import re
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    """Base class for all record fields."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Represents a contact's name. Cannot be empty."""
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    """Represents and validates a phone number."""
    def __init__(self, value):
        # Remove common formatting characters
        cleaned_value = re.sub(r"[\+\(\)\-\s]", "", value)
      
        # Normalize Ukrainian prefix (+380) to 10 digits
        if len(cleaned_value) == 12 and cleaned_value.startswith("380"):
            cleaned_value = cleaned_value[2:]
            
        if not self._validate_phone(cleaned_value):
            raise ValueError("Invalid phone format. Use 10 digits (e.g., 0981234567) or +380 format.")
            
        super().__init__(cleaned_value)

    def _validate_phone(self, value):
        # Ensure the phone is exactly 10 digits long and contains only numbers
        return len(value) == 10 and value.isdigit()

class Email(Field):
    """Represents and validates an email address using Regex."""
    def __init__(self, value):
        if not self._validate_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    def _validate_email(self, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, value) is not None

class Address(Field):
    """Represents a physical address. Cannot be empty."""
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)

class Birthday(Field):
    """Represents and validates a contact's birthday."""
    def __init__(self, value):
        formats = ["%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y"]
        
        for fmt in formats:
            try:
                # Attempt to parse the date using supported formats
                self.date = datetime.strptime(value, fmt).date()
                
                # Prevent future dates
                if self.date > datetime.today().date():
                    raise ValueError("Birthday cannot be in the future.")
                
                # Store the normalized string format internally
                normalized_value = self.date.strftime("%d.%m.%Y")
                super().__init__(normalized_value)
                return
                
            except ValueError as e:
                # Re-raise error if it's the future-date validation error
                if "future" in str(e):
                    raise e
                continue
                
        raise ValueError("Invalid date format. Use DD.MM.YYYY, DD/MM/YYYY or DD-MM-YYYY")
    
class Record:
    """Stores contact information including name, phones, birthday, email, and address."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number):
        # Adds a phone number, preventing duplicates
        new_phone = Phone(phone_number)
        if new_phone.value in [p.value for p in self.phones]:
            raise ValueError(f"Phone number {new_phone.value} already exists for this contact.")
        self.phones.append(new_phone)

    def remove_phone(self, phone_number):
        # Rebuilds the phones list excluding the specified number
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone, new_phone):
        # Updates an existing phone number
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            phone_obj.value = Phone(new_phone).value
        else:
            raise ValueError(f"Phone {old_phone} not found in this record.")

    def find_phone(self, phone_number):
        # Searches for a phone object by its string value
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
        # Formats the record details for console output
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        email_str = f", email: {self.email.value}" if self.email else ""
        address_str = f", address: {self.address.value}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}{email_str}{address_str}"


class AddressBook(UserDict):
    """Manages a collection of Record objects using names as keys."""
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find_contacts(self, query: str):
        """Searches for contacts by partial name or phone match."""
        result = []
        query = query.lower()
        
        for record in self.data.values():
            # Check for name match
            if query in record.name.value.lower():
                result.append(record)
                continue
                
            # Check for phone match
            for phone in record.phones:
                if query in phone.value:
                    result.append(record)
                    break
                    
        return result

    def get_birthdays_per_range(self, days: int):
        """Returns a list of upcoming birthdays within a specified number of days."""
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
                
            birthday_date = record.birthday.date
            
            # Handle leap year edge case (Feb 29th)
            try:
                birthday_this_year = birthday_date.replace(year=today.year)
            except ValueError:
                birthday_this_year = birthday_date.replace(year=today.year, month=3, day=1)

            # If the birthday has already passed this year, look at next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_delta = (birthday_this_year - today).days

            # Check if the birthday falls within the requested time frame
            if 0 <= days_delta <= days:
                congratulation_date = birthday_this_year

                # Shift weekend birthdays to the following Monday
                if congratulation_date.weekday() == 5: # Saturday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6: # Sunday
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays