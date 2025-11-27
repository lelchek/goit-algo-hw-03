from typing import Callable
from functools import wraps


def input_error(func: Callable):
    """Decorator that handles common input-related errors"""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Error: Give me a name and a phone, please."

        except KeyError:
            return "Error: Contact does not exist"

        except IndexError:
            return "Error: Give me a name, please."

    return inner


def parse_input(user_input: str):
    """Parses user input into a command and arguments"""

    parts = user_input.split()

    if not parts:
        return "", []

    cmd, *args = parts
    cmd = cmd.lower().strip()
    args = [arg.lower().strip() for arg in args]

    return cmd, args


def greeting():
    """Returns a greeting message"""

    return "How can I help you?"


@input_error
def add_contact(args, contacts):
    """Adds a new contact to the phone book"""

    name, phone = args

    if name not in contacts:
        contacts[name] = phone
        return "Contact added."
    else:
        return "Error: Contact already exists"


@input_error
def change_contact(args, contacts):
    """Updates an existing contact’s phone number"""

    name, phone = args

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """Displays the phone number for a given contact"""

    name = args[0]

    return f"Phone number for {name} is {contacts[name]}."


def show_all(contacts):
    """Shows all contacts in the phone book"""

    if not contacts:
        return "No contacts found."

    contact_list = ""

    for name, phone in contacts.items():
        contact_list += f"{name}: {phone}\n"

    return contact_list.strip()


def bye():
    """Returns a goodbye message"""

    return "Good bye!"


def main():
    """Entry point for the assistant bot"""

    contacts = {}

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        match command:
            case "hello":
                print(greeting())

            case "add":
                print(add_contact(args, contacts))

            case "change":
                print(change_contact(args, contacts))

            case "phone":
                print(show_phone(args, contacts))

            case "all":
                print(show_all(contacts))

            case "close" | "exit":
                print(bye())
                break

            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
