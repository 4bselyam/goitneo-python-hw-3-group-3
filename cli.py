from core import AddressBook, Phone, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input provided. Please check your input and try again."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), args


@input_error
def add_contact(args, address_book):
    if len(args) < 2:
        raise IndexError
    name, phone = args
    record = Record(name, phone)
    address_book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, address_book):
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    if name in address_book.records:
        address_book.records[name].phones = [Phone(phone)]
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args, address_book):
    if not args:
        raise IndexError
    name = args[0]
    if name in address_book.records:
        return ", ".join([str(phone) for phone in address_book.records[name].phones])
    else:
        raise KeyError


@input_error
def show_all(address_book):
    if not address_book.records:
        return "No contacts saved."
    return "\n".join([str(record) for record in address_book.records.values()])


@input_error
def add_birthday_command(args, address_book):
    if len(args) < 2:
        raise IndexError
    name, birthday = args
    if name in address_book.records:
        address_book.records[name].add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError


@input_error
def show_birthday_command(args, address_book):
    if not args:
        raise IndexError
    name = args[0]
    if name in address_book.records and address_book.records[name].birthday:
        return str(address_book.records[name].birthday)
    else:
        raise KeyError


@input_error
def birthdays_command(address_book):
    birthdays = address_book.get_birthdays_per_week()
    if not birthdays:
        return "No birthdays this week."
    return "\n".join(birthdays)


def execute_command(command, args, address_book):
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": lambda address_book: show_all(address_book),
        "add-birthday": add_birthday_command,
        "show-birthday": show_birthday_command,
        "birthdays": birthdays_command,
    }

    if command in ["close", "exit"]:
        print("Good bye!")
        return False
    elif command == "hello":
        print("How can I help you?")
    elif command in commands:
        if command in ["all", "birthdays"]:
            print(commands[command](address_book))
        else:
            print(commands[command](args, address_book))
    else:
        print("Invalid command.")
    return True


def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if not execute_command(command, args, address_book):
            break


if __name__ == "__main__":
    main()
