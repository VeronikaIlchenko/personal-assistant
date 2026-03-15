# 🌟 Pythonator3000 - Personal Assistant CLI

🤖 Pythonator3000: Command-line productivity made effortless. > It's simple yet deeply powerful, allowing you to manage your address book and notes with zero hustle. We designed this tool for users who value their time: execute quick commands to get things done instantly, and let our adaptive menus guide you only when making precise edits. No endless Q&A, no bloated interfaces — just smart fuzzy-search, strict data validation, and pure CLI efficiency.

## ✨ Key Features

### 👤 Smart Contact Management

- **Hybrid Input**: Add contacts instantly or use step-by-step interactive menus for detailed records
- **Robust Validation**: Smart phone number normalization (automatically handles +380, spaces, brackets, and dashes), multi-format birthday support (DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY) with future-date prevention, and strict email format checks.
- **Rich Profiles**: Support for multiple phone numbers, physical addresses, emails, and birthdays per contact
- **Birthday Tracking**: A dedicated system to monitor upcoming birthdays within a custom range

### 📝 Advanced Note System

- **Tagging**: Add unlimited tags to your notes for quick grouping and filtering
- **Interactive Editor**: Modify note text or manage tags through a dedicated submenu
- **ID-Based Access**: Every note is assigned a unique ID for fast searching and deletion

### 🧠 Intelligent UX (User Experience)

- **Fuzzy Search**: Typo-tolerant command recognition (e.g., `ad-contct` → `add-contact`)
- **Smart Command Merge**: Understands commands entered with spaces (e.g., `all contacts` instead of `all-contacts`)
- **Adaptive Tables**: Text-wrapping logic ensures long notes or emails never break the table layout

## � Installation & Setup

This project is configured as a Python package, allowing you to install it and run it from any directory on your system.

### Prerequisites

Ensure you have Python 3.8 or higher installed.

### Install the Package

Navigate to the project's root directory (where `setup.py` is located) and run:

```bash
# For macOS and Linux:
python3 -m pip install -e .

# For Windows:
pip install -e .
```

### Launch the App

Once installed, start the assistant from any terminal window simply by typing:

```bash
assistant
```

Or run directly from the project root:

```bash
python src/main.py
```

## 📂 Project Structure

The project follows a modular architecture for high maintainability:

- `src/main.py` – Core application loop and command dispatcher
- `src/models/` – Object-Oriented logic for `AddressBook` and `NoteBook`
- `src/utils/` – Error handling, field validation, and fuzzy search logic
- `src/storage.py` – Reliable data persistence in the user's home directory (`~/.personal_assistant_data`)

## � Popular Commands

| Command | Description |
|---|---|
| `add-contact <name>` | Add a new contact |
| `show-contact <name>` | Show all details for a specific contact |
| `all-contacts` | Show list of all contacts |
| `search-contact <query>` | Search contacts by name or phone |
| `edit-contact <name>` | ⚙️Interactive: Edit name, phone, email, etc. |
| `remove-field <name>` | ⚙️Interactive: Remove specific fields |
| `delete-contact <name>` | Delete the entire contact record |
| `show-birthdays [days]` | Show upcoming birthdays (default: 7 days) |
| `add-birthday <name> <date>` | Quick add: Birthday (DD.MM.YYYY) |
| `add-note [text]` | ⚙️Interactive: Create a new note with tags |
| `show-notes` | Show all notes |
| `search-notes <query>` | Search notes by text |
| `search-tags <tag1> [tag2...]` | Search notes by specific tags |
| `edit-note <id>` | ⚙️Interactive: Edit text or tags |
| `delete-note <id>` | Delete a specific note |
| `help` | Show the help menu |
| `exit` / `close` | Save data and quit |

## 👥 Team 

This project was built collaboratively using Agile/Scrum methodologies:

- **Veronika Ilchenko (Team Lead)**: Architecture, data persistence, and core logic
- **Alisa Skrypnyk (Developer)**: Address book models and data validation
- **Yaroslav Ivanchenko (Developer & Scrum Master)**: Note system, UX interface, packaging, and documentation



