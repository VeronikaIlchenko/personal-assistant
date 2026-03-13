import sys
from storage import load_data, save_data
from models.address_book import AddressBook, Record
from models.notes import NoteBook
from utils.handlers import input_error
from utils.fuzzy_search import suggest_command


COMMANDS = [
    "hello", "add-contact", "phone", "all-contacts", 
    "add-birthday", "birthdays", "add-note", "edit-note", 
    "delete-note", "search-notes", "search-tags", "all-notes", 
    "close", "exit"
]

def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "✅ Contact added."
    else:
        message = "✅ Contact updated."
    record.add_phone(phone)
    return message

@input_error
def show_phone(args, book: AddressBook):
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    raise KeyError

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "🎂 Birthday added."
    raise KeyError

@input_error
def show_birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    birthdays = book.get_birthdays_per_range(days)
    if not birthdays:
        return f"📅 No birthdays in the next {days} days."
    res = [f"🎂 {item['name']}: {item['congratulation_date']}" for item in birthdays]
    return "\n".join(res)


@input_error
def add_note(args, notes: NoteBook):
    if not args:
        raise IndexError
    text = args[0]
    tags = args[1:] if len(args) > 1 else None
    note_id = notes.add_note(text, tags)
    return f"📝 Note added with ID: {note_id}"

@input_error
def search_notes(args, notes: NoteBook):
    if not args:
        raise IndexError
    query = args[0]
    results = notes.search_by_text(query)
    if not results:
        return "🔍 No notes found."
    return "\n".join([f"ID {nid}: {note}" for nid, note in results])

@input_error
def search_tags(args, notes: NoteBook):
    if not args:
        raise IndexError
    results = notes.search_by_tags(args)
    if not results:
        return "🏷️ No notes found with these tags."
    return "\n".join([f"ID {nid}: {note}" for nid, note in results])



def main():
    book = load_data("addressbook.pkl", AddressBook)
    notes = load_data("notes.pkl", NoteBook)
    
    print("\n🌟 Welcome to Personal Assistant CLI!")
    print(f"Commands: {', '.join(COMMANDS[:5])}... (type 'exit' to quit)")
    
    while True:
        try:
            user_input = input("\n🔹 Enter command: ").strip()
            if not user_input:
                continue
                
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book, "addressbook.pkl")
                save_data(notes, "notes.pkl")
                print("👋 Good bye! All data saved safely.")
                break
            
            elif command == "hello":
                print("How can I help you?")

         
            elif command == "add-contact":
                print(add_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all-contacts":
                if not book.data:
                    print("📭 Address book is empty.")
                for record in book.data.values():
                    print(record)
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "birthdays":
                print(show_birthdays(args, book))

            elif command == "add-note":
                print(add_note(args, notes))
            elif command == "search-notes":
                print(search_notes(args, notes))
            elif command == "search-tags":
                print(search_tags(args, notes))
            elif command == "all-notes":
                if not notes.data:
                    print("🗒️ NoteBook is empty.")
                for nid, note in notes.data.items():
                    print(f"ID {nid}: {note}")

            else:
                suggestion = suggest_command(command, COMMANDS)
                if suggestion:
                    print(f"❓ Unknown command. Did you mean '{suggestion}'?")
                else:
                    print("❓ Unknown command. Type 'exit' to save and quit.")
                
        except KeyboardInterrupt:
            save_data(book, "addressbook.pkl")
            save_data(notes, "notes.pkl")
            print("\n⚠️ Forced shutdown. Data saved safely.")
            sys.exit()

if __name__ == "__main__":
    main()