import sys
from storage import load_data, save_data
from models.address_book import AddressBook
from models.notes import NoteBook 

def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args

def main():
    book = load_data("addressbook.pkl", AddressBook)
    notes = load_data("notes.pkl", NoteBook)
    
    print("🌟 Welcome to Personal Assistant CLI!")
    
    while True:
        try:
            user_input = input("Enter a command: ").strip()
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book, "addressbook.pkl")
                save_data(notes, "notes.pkl")
                print("👋 Good bye! All data saved.")
                break
            
            elif command == "hello":
                print("How can I help you?")

            else:
                print("❓ Invalid command.")
                
        except KeyboardInterrupt:
            save_data(book, "addressbook.pkl")
            save_data(notes, "notes.pkl")
            print("\n⚠️ Forced shutdown. Data saved safely.")
            sys.exit()

if __name__ == "__main__":
    main()