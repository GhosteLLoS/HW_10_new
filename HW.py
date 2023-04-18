from collections import UserDict


class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    

class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name:Name, phone:Phone=None) -> None:
        self.name = name
        self.phones = [phone] if phone else []

    def __str__(self):
        return str(self.phones)
    
    def __repr__(self):
        return str(self.phones)
    
    def add_number(self, phone:Phone):
        self.phones.append(phone)
    
    def del_phone(self, phone):
        for i, p in enumerate(self.phones):
            if p.value == phone.value:
                return self.phones.pop(i)
    
    def change_phone(self, old_phone, new_phone):
        del_phone = self.del_phone(old_phone)
        if del_phone:
            self.add_number(new_phone)
            return True
        return False
    

    
class Addressbook(UserDict):
    def add_record(self, rec:Record):
        self.data[rec.name.value] = rec


contacts = Addressbook()


def input_errors(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, IndexError, ValueError):
            return "Not enough arguments."
    return inner


@input_errors
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = contacts.get(name.value)
    if rec:
        rec.add_number(phone)
        return f'phone number {phone} added successfully to contact {name}'
    rec = Record(name, phone)
    contacts.add_record(rec)
    return f'contact {name} with phone number {phone} added successfully'


@input_errors
def change_phone_number(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    if contacts.get(name.value):
        contacts[name.value].change_phone(old_phone, new_phone)
        return f"Phone number for contact {name} changed"
    return f"No contact with name {name}"


@input_errors
def print_phone_number(*args):
    name = Name(args[0])
    # phone = Phone(args[1])
    rec = contacts.get(name.value)
    if rec:
        return rec.phones
    return f"No contact with name {name}"


def show_all(*args):
    if contacts:
        return '\n'.join([f'{name}: {phone}' for name, phone in contacts.items()])
    return "You have no contacts yet"


def hello(*args):
    return "How can I help you?"


def good_bye(*args):
    return 'Good bye!'


def no_command(*args):
    return "Unknown command, try again"


COMMANDS = {'hello': hello,
            'add': add,
            'good bye': good_bye,
            'exit': good_bye,
            'close': good_bye,
            'show all': show_all,
            'change': change_phone_number,
            'phone': print_phone_number,
           
}


def command_handler(text):
    for kword, command in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip().split()
    return no_command, None


def main():
    print(hello())
    while True:
        user_input = (input(">>>")) 
        command, data = command_handler(user_input)
        print(command(*data))
        if command == good_bye:
            break
            

if __name__ == '__main__':
    main()
