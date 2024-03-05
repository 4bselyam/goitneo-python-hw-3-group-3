from datetime import datetime, timedelta
import re
import json


class Birthday:
    def __init__(self, birthday):
        self.birthday = None
        self.set_birthday(birthday)

    def set_birthday(self, birthday):
        if not re.match(r"\d{2}\.\d{2}\.\d{4}", birthday):
            raise ValueError("Birthday must be in DD.MM.YYYY format.")
        self.birthday = datetime.strptime(birthday, "%d.%m.%Y")

    def __str__(self):
        return self.birthday.strftime("%d.%m.%Y")


class Phone:
    def __init__(self, phone):
        self.phone = None
        self.set_phone(phone)

    def set_phone(self, phone):
        if not re.match(r"\d{10}", phone):
            raise ValueError("Phone number must contain 10 digits.")
        self.phone = phone

    def __str__(self):
        return self.phone


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = None
        if phone:
            self.add_phone(phone)
        if birthday:
            self.add_birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = ", ".join([str(phone) for phone in self.phones])
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name}: {phones_str}{birthday_str}"


class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name] = record

    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        birthdays_this_week = []
        for record in self.records.values():
            if record.birthday and today <= record.birthday.birthday <= next_week:
                birthdays_this_week.append(record.name)
        return birthdays_this_week

    def save_to_file(self, file_name):
        with open(file_name, "w") as file:
            json_data = {
                name: {
                    "phones": [phone.phone for phone in record.phones],
                    "birthday": (
                        record.birthday.birthday.strftime("%d.%m.%Y")
                        if record.birthday
                        else None
                    ),
                }
                for name, record in self.records.items()
            }
            json.dump(json_data, file, indent=4)

    def load_from_file(self, file_name):
        with open(file_name, "r") as file:
            json_data = json.load(file)
            for name, data in json_data.items():
                record = Record(name)
                for phone in data["phones"]:
                    record.add_phone(phone)
                if data["birthday"]:
                    record.add_birthday(data["birthday"])
                self.add_record(record)
