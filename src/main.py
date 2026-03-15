import sys
import textwrap
from datetime import datetime
from typing import Tuple

# Enables arrow-key navigation in the terminal if supported by the OS
try:
    import readline
except ImportError:
    pass 

from storage import load_data, save_data
from models.address_book import AddressBook, Record
from models.notes import NoteBook
from utils.fuzzy_search import suggest_command
from utils.handlers import input_error

# Registry of all available CLI commands
COMMANDS = [
    "hello", "help", "add-contact", "show-contact", "all-contacts", 
    "add-birthday", "show-birthdays", "add-email", "add-address", 
    "search-contact", "edit-contact", "remove-field", "delete-contact",
    "add-note", "search-notes", "search-tags", "show-notes", 
    "edit-note", "delete-note", "close", "exit"
]

def parse_input(user_input: str) -> Tuple[str, list]:
    # Parses raw user input into a standardized command string and a list of arguments
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args

@input_error
def add_contact(args: list, book: AddressBook) -> str:
    # Adds a new contact or triggers the interactive setup if no phone is provided
    if not args:
        raise IndexError
        
    name = args[0]
    record = book.find(name)
    is_new = False
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        is_new = True

    if len(args) == 2:
        phone = args[1]
        record.add_phone(phone)
        if is_new:
            return f"✅ Contact '{name}' created and phone {phone} added."
        else:
            return f"✅ Phone {phone} added to existing contact '{name}'."

    if is_new:
        print(f"✅ Contact '{name}' created! Let's add some details.")
    else:
        print(f"⚡ Contact '{name}' already exists. Let's update details.")
            
    return edit_contact([name], book)

@input_error
def show_contact(args: list, book: AddressBook) -> str:
    # Displays all stored details for a specific contact
    if not args:
        raise IndexError
    name = " ".join(args)
    record = book.find(name)
    if record:
        return str(record)
    raise KeyError

@input_error
def search_contact(args: list, book: AddressBook) -> str:
    # Searches for contacts by matching the query against names and phone numbers
    if not args:
        raise IndexError
    query = args[0]
    results = book.find_contacts(query)
    if not results:
        return "🔍 No contacts found."
    
    res = ["\n🔍 FOUND CONTACTS:"]
    for record in results:
        res.append(str(record))
    return "\n".join(res)

@input_error
def edit_contact(args: list, book: AddressBook) -> str:
    # Interactive CLI wizard to modify existing contact fields
    if not args:
        raise IndexError
    name = " ".join(args)
    record = book.find(name)
    if not record:
        raise KeyError
        
    while True:
        print(f"\n👉 What do you want to edit/add for {name}?")
        print("  [1] Name\n  [2] Phone\n  [3] Email\n  [4] Address\n  [5] Birthday\n  [0] Finish / Exit menu")
        choice = input("Select an option (0-5): ").strip()
        
        try:
            if choice == '0':
                return f"⏭️  Finished with contact '{name}'."
                
            elif choice == '1':
                new_name = input("👉 Enter new name: ").strip()
                while True:
                    if not new_name:
                        raise ValueError("Name cannot be empty.")
                    if book.find(new_name):
                        print(f"⚠️ Contact '{new_name}' already exists.")
                        new_name = input("👉 Please add a surname or enter a different name: ").strip()
                    else:
                        break
                        
                book.data[new_name] = book.data.pop(name)
                record.name.value = new_name
                name = new_name
                print(f"✅ Name updated to {new_name}.")
                
            elif choice == '2':
                if not record.phones:
                    new_phone = input("👉 Enter new phone: ").strip()
                    record.add_phone(new_phone)
                    print("✅ Phone added.")
                else:
                    print("Current phones:")
                    for i, p in enumerate(record.phones, 1):
                        print(f"  [{i}] {p.value}")
                    idx = input("Select phone to edit (or press Enter to add a new one): ").strip()
                    
                    if not idx:
                        new_phone = input("👉 Enter new phone: ").strip()
                        record.add_phone(new_phone)
                        print("✅ Additional phone added.")
                    else:
                        try:
                            idx = int(idx) - 1
                            old_phone = record.phones[idx].value
                        except (ValueError, IndexError):
                            raise ValueError("Invalid selection.")
                        new_phone = input("👉 Enter new phone: ").strip()
                        record.edit_phone(old_phone, new_phone)
                        print("✅ Phone updated.")
                
            elif choice == '3':
                new_email = input("👉 Enter new email: ").strip()
                record.add_email(new_email)
                print("✅ Email updated.")
                
            elif choice == '4':
                new_address = input("👉 Enter new address: ").strip()
                record.add_address(new_address)
                print("✅ Address updated.")
                
            elif choice == '5':
                new_birthday = input("👉 Enter new birthday (e.g., 15.03.1990): ").strip()
                record.add_birthday(new_birthday)
                print("✅ Birthday updated.")
                
            else:
                print("❌ Invalid choice. Please select 0-5.")
                
        except ValueError as e:
            print(f"❌ Data error: {e}")

@input_error
def remove_field(args: list, book: AddressBook) -> str:
    # Interactive CLI wizard to selectively delete fields from a contact
    if not args:
        raise IndexError
    name = " ".join(args)
    record = book.find(name)
    if not record:
        raise KeyError
        
    while True:
        print(f"\n👉 What do you want to remove from {name}?")
        print("  [1] Phone\n  [2] Email\n  [3] Address\n  [4] Birthday\n  [0] Finish / Exit menu")
        choice = input("Select an option (0-4): ").strip()
        
        if choice == '0':
            return "⏭️  Removal menu closed."
            
        elif choice == '1':
            if not record.phones:
                print("⚠️ No phones to remove.")
            else:
                print("Current phones:")
                for i, p in enumerate(record.phones, 1):
                    print(f"  [{i}] {p.value}")
                idx = input("Select phone to remove: ").strip()
                try:
                    idx = int(idx) - 1
                    phone_to_remove = record.phones[idx].value
                    record.remove_phone(phone_to_remove)
                    print("✅ Phone removed.")
                except (ValueError, IndexError):
                    print("❌ Data error: Invalid selection.")
            
        elif choice == '2':
            if record.email:
                record.email = None
                print("✅ Email removed.")
            else:
                print("⚠️ No email to remove.")
            
        elif choice == '3':
            if record.address:
                record.address = None
                print("✅ Address removed.")
            else:
                print("⚠️ No address to remove.")
            
        elif choice == '4':
            if record.birthday:
                record.birthday = None
                print("✅ Birthday removed.")
            else:
                print("⚠️ No birthday to remove.")
            
        else:
            print("❌ Invalid choice. Please select 0-4.")

@input_error
def delete_contact(args: list, book: AddressBook) -> str:
    # Permanently removes a contact from the address book
    if not args:
        raise IndexError
    name = " ".join(args)
    if book.find(name):
        book.delete(name)
        return "🗑️ Contact deleted."
    raise KeyError

@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    # Appends a birthday to an existing contact
    if len(args) < 2:
        raise IndexError
    birthday = args[-1]
    name = " ".join(args[:-1])
    
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "🎂 Birthday added."
    raise KeyError

@input_error
def add_email(args: list, book: AddressBook) -> str:
    # Appends an email address to an existing contact
    if len(args) < 2:
        raise IndexError
    email = args[-1]
    name = " ".join(args[:-1])
    
    record = book.find(name)
    if record:
        record.add_email(email)
        return "📧 Email added."
    raise KeyError

@input_error
def add_address(args: list, book: AddressBook) -> str:
    # Appends a physical address to an existing contact
    if len(args) < 2:
        raise IndexError
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record:
        record.add_address(address)
        return "🏠 Address added."
    raise KeyError

@input_error
def show_birthdays(args: list, book: AddressBook) -> str:
    # Returns a list of contacts with birthdays within the specified timeframe (default 7 days)
    days = int(args[0]) if args else 7
    birthdays = book.get_birthdays_per_range(days)
    if not birthdays:
        return f"📅 No birthdays in the next {days} days."
    res = [f"🎂 {item['name']}: {item['congratulation_date']}" for item in birthdays]
    return "\n".join(res)

@input_error
def add_note(args: list, notes: NoteBook) -> str:
    # Creates a new note, either inline or via interactive prompts
    if args:
        text = " ".join(args)
    else:
        text = input("👉 Enter your note: ").strip()
        if not text:
            raise ValueError("Note text cannot be empty.")
            
    tag_input = input("👉 Enter tags for the note (space-separated, or press Enter to skip): ").strip()
    tags = [tag.strip() for tag in tag_input.split()] if tag_input else []
        
    note_id = notes.add_note(text, tags)
    return f"📝 Note added with ID: {note_id}"

@input_error
def search_notes(args: list, notes: NoteBook) -> str:
    # Searches the notebook by note text content
    if not args:
        raise IndexError
    query = " ".join(args)
    results = notes.search_by_text(query)
    if not results:
        return "🔍 No notes found."
    return "\n".join([f"ID {nid}: {note}" for nid, note in results])

@input_error
def search_tags(args: list, notes: NoteBook) -> str:
    # Searches the notebook for specific tags
    if not args:
        raise IndexError
    results = notes.search_by_tags(args)
    if not results:
        return "🏷️ No notes found with these tags."
    return "\n".join([f"ID {nid}: {note}" for nid, note in results])

@input_error
def edit_note(args: list, notes: NoteBook) -> str:
    # Interactive CLI wizard to modify existing note text or tags
    if not args:
        raise IndexError
        
    try:
        note_id = int(args[0])
    except ValueError:
        raise ValueError("Note ID must be a number.")
        
    if note_id not in notes.data:
        raise KeyError
        
    note = notes.data[note_id]
    
    while True:
        print(f"\n👉 What do you want to edit for Note ID {note_id}?")
        print("  [1] Edit Text\n  [2] Add Tag\n  [3] Remove Tag\n  [0] Finish / Exit menu")
        choice = input("Select an option (0-3): ").strip()
        
        try:
            if choice == '0':
                return f"⏭️  Finished editing Note ID {note_id}."
                
            elif choice == '1':
                print(f"Current text: {note.text}")
                new_text = input("👉 Enter new text: ").strip()
                if not new_text:
                    raise ValueError("Note text cannot be empty.")
                notes.edit_note(note_id, new_text)
                print("✅ Note text updated.")
                
            elif choice == '2':
                new_tag = input("👉 Enter new tag: ").strip()
                if not new_tag:
                    raise ValueError("Tag cannot be empty.")
                note.add_tag(new_tag)
                print(f"✅ Tag '{new_tag}' added.")
                
            elif choice == '3':
                if not note.tags:
                    print("⚠️ No tags to remove.")
                else:
                    print(f"Current tags: {', '.join(note.tags)}")
                    tag_to_remove = input("👉 Enter tag to remove: ").strip()
                    note.remove_tag(tag_to_remove)
                    print(f"✅ Tag '{tag_to_remove}' removed.")
                    
            else:
                print("❌ Invalid choice. Please select 0-3.")
                
        except ValueError as e:
            print(f"❌ Data error: {e}")

@input_error
def delete_note(args: list, notes: NoteBook) -> str:
    # Permanently removes a note by its ID
    if not args:
        raise IndexError
        
    try:
        note_id = int(args[0])
    except ValueError:
        raise ValueError("Note ID must be a number.")
        
    if note_id in notes.data:
        notes.delete_note(note_id)
        return f"🗑️ Note ID {note_id} deleted."
    raise KeyError

def show_help() -> str:
    # Returns the formatted help menu string
    return """
🌟 Here is what I can do for you:

👤 CONTACTS (CORE)
  • add-contact <name>                  👉 Add a new contact
  • show-contact <name>                 👉 Show all details for a specific contact
  • all-contacts                        👉 Show list of all contacts
  • search-contact <query>              👉 Search contacts by name or phone

🛠️ CONTACTS (MANAGEMENT)
  • edit-contact <name>                 👉 ⚙️ Interactive: Edit name, phone, email, etc.
  • remove-field <name>                 👉 ⚙️ Interactive: Remove specific fields
  • delete-contact <name>               👉 Delete the entire contact record

📅 BIRTHDAYS
  • show-birthdays [days]               👉 Show upcoming birthdays (default: 7 days)
  • add-birthday <name> <date>          👉 Quick add: Birthday (DD.MM.YYYY)

📝 NOTES
  • add-note [text]                     👉 ⚙️ Interactive: Create a new note with tags
  • show-notes                          👉 Show all notes
  • search-notes <query>                👉 Search notes by text
  • search-tags <tag1> [tag2...]        👉 Search notes by specific tags
  • edit-note <id>                      👉 ⚙️ Interactive: Edit text or tags
  • delete-note <id>                    👉 Delete a specific note

👋 SYSTEM
  • help                                👉 Show this menu
  • exit / close                        👉 Save data and quit
"""

def main():
    # Initialize storage and fix note ID counters upon startup
    book = load_data("addressbook.pkl", AddressBook)
    notes = load_data("notes.pkl", NoteBook)
    
    if notes.data:
        max_id = max(notes.data.keys())
        notes.set_id_counter(max_id)
    
    print("\n🤖 Welcome to Pythonator3000 - Personal Assistant CLI!")
    print(show_help())
    
    # Main CLI execution loop
    while True:
        try:
            user_input = input("\n🔹 Enter command: ").strip()
            if not user_input:
                continue
                
            command, args = parse_input(user_input)

            # Smart UX routing: Handle multi-word commands (e.g., "all contacts" -> "all-contacts")
            if args and f"{command}-{args[0]}" in COMMANDS:
                command = f"{command}-{args[0]}"
                args = args[1:]

            if command in ["close", "exit"]:
                save_data(book, "addressbook.pkl")
                save_data(notes, "notes.pkl")
                print("👋 Good bye! All data saved safely.")
                break
            
            elif command == "hello":
                print("How can I help you?")
                
            elif command == "help":
                print(show_help())

            elif command == "add-contact":
                print(add_contact(args, book))
                
            elif command == "show-contact":
                print(show_contact(args, book))
                
            elif command == "search-contact":
                print(search_contact(args, book))
                
            elif command == "edit-contact":
                print(edit_contact(args, book))
                
            elif command == "remove-field":
                print(remove_field(args, book))
                
            elif command == "delete-contact":
                print(delete_contact(args, book))
                
            elif command == "add-email":
                print(add_email(args, book))
                
            elif command == "add-address":
                print(add_address(args, book))
                
            elif command == "all-contacts":
                # Render formatted ASCII table for contacts with dynamic text wrapping
                if not book.data:
                    print("📭 Address book is empty.")
                else:
                    print("\n📱 ALL CONTACTS:")
                    print("-" * 102)
                    print(f"| {'NAME':<15} | {'PHONES':<20} | {'BIRTHDAY':<10} | {'EMAIL':<20} | {'ADDRESS':<20} |")
                    print("-" * 102)
                    for record in book.data.values():
                        name_str = str(getattr(record, 'name', 'Unknown'))
                        phones_str = ", ".join(str(p) for p in getattr(record, 'phones', [])) or "-"
                        
                        b_val = getattr(record, 'birthday', None)
                        birthday_str = str(b_val.value) if b_val else "-"
                        
                        e_val = getattr(record, 'email', None)
                        email_str = str(e_val.value) if e_val else "-"
                        
                        a_val = getattr(record, 'address', None)
                        address_str = str(a_val.value) if a_val else "-"
                        
                        name_lines = textwrap.wrap(name_str, 15) or ["-"]
                        phones_lines = textwrap.wrap(phones_str, 20) or ["-"]
                        birthday_lines = textwrap.wrap(birthday_str, 10) or ["-"]
                        email_lines = textwrap.wrap(email_str, 20) or ["-"]
                        address_lines = textwrap.wrap(address_str, 20) or ["-"]
                        
                        max_lines = max(len(name_lines), len(phones_lines), len(birthday_lines), len(email_lines), len(address_lines))
                        
                        for i in range(max_lines):
                            n = name_lines[i] if i < len(name_lines) else ""
                            p = phones_lines[i] if i < len(phones_lines) else ""
                            b = birthday_lines[i] if i < len(birthday_lines) else ""
                            e = email_lines[i] if i < len(email_lines) else ""
                            a = address_lines[i] if i < len(address_lines) else ""
                            
                            print(f"| {n:<15} | {p:<20} | {b:<10} | {e:<20} | {a:<20} |")
                        print("-" * 102)
                    
            elif command == "add-birthday":
                print(add_birthday(args, book))
                
            elif command == "show-birthdays":
                print(show_birthdays(args, book))

            elif command == "add-note":
                print(add_note(args, notes))
                
            elif command == "edit-note":
                print(edit_note(args, notes))
                
            elif command == "delete-note":
                print(delete_note(args, notes))
                
            elif command == "search-notes":
                print(search_notes(args, notes))
                
            elif command == "search-tags":
                print(search_tags(args, notes))
                
            elif command == "show-notes":
                # Render formatted ASCII table for notes with dynamic text wrapping
                if not notes.data:
                    print("🗒️ NoteBook is empty.")
                else:
                    print("\n🗒️  ALL NOTES:")
                    print("-" * 80)
                    print(f"| {'ID':<4} | {'NOTE TEXT':<45} | {'TAGS':<20} |")
                    print("-" * 80)
                    
                    for nid, note in notes.data.items():
                        text_val = str(note.text)
                        tags_val = ", ".join(note.tags) if note.tags else "-"
                        
                        text_lines = textwrap.wrap(text_val, 45) or ["-"]
                        tags_lines = textwrap.wrap(tags_val, 20) or ["-"]
                        id_lines = [str(nid)]
                        
                        max_lines = max(len(text_lines), len(tags_lines), len(id_lines))
                        
                        for i in range(max_lines):
                            id_str = id_lines[i] if i < len(id_lines) else ""
                            t_str = text_lines[i] if i < len(text_lines) else ""
                            tag_str = tags_lines[i] if i < len(tags_lines) else ""
                            
                            print(f"| {id_str:<4} | {t_str:<45} | {tag_str:<20} |")
                        print("-" * 80)

            else:
                # Fallback: Suggest a similar command using fuzzy matching if the user makes a typo
                potential_cmd = f"{command}-{args[0]}" if args else command
                suggestion = suggest_command(potential_cmd, COMMANDS) or suggest_command(command, COMMANDS)
                
                if suggestion:
                    print(f"❓ Unknown command. Did you mean '{suggestion}'?")
                else:
                    print("❓ Unknown command. Type 'help' to see available commands or 'exit' to quit.")
                
        except KeyboardInterrupt:
            # Handles unexpected exits (Ctrl+C) securely by saving the data
            save_data(book, "addressbook.pkl")
            save_data(notes, "notes.pkl")
            print("\n⚠️ Forced shutdown. Data saved safely.")
            sys.exit()

if __name__ == "__main__":
    main()