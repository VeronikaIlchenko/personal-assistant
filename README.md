# 🌟 Personal Assistant CLI

Personal Assistant CLI is a powerful, interactive command-line tool designed to help you manage your contacts and notes with ease. Built with a focus on User Experience (UX), it features smart command recognition, robust data validation, and an adaptive interface.

## ✨ Key Features

### 👤 Smart Contact Management

- **Hybrid Input**: Add contacts instantly or use step-by-step interactive menus for detailed records
- **Robust Validation**: Automatic checks for phone numbers (10 digits), email formats, and dates
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
|---------|-------------|
| `add-contact <name>` | Create a new contact via interactive menu |
| `show-contact <name>` | Display all details for a specific contact |
| `all-contacts` | View a formatted table of all contacts |
| `show-birthdays [days]` | List contacts with upcoming birthdays |
| `add-note [text]` | Create a new note with optional tags |
| `edit-note <id>` | Modify text or tags for a specific note |
| `show-notes` | View all notes in a clean, wrapped table |
| `help` | View the full list of available commands |
| `exit` / `close` | Save data and quit |

## 👥 Team 

This project was built collaboratively using Agile/Scrum methodologies:

- **Veronika (Team Lead)**: Architecture, data persistence, and core logic
- **Alisa (Developer)**: Address book models and data validation
- **Yaroslav (Developer & Scrum Master)**: Note system, UX interface, packaging, and documentation



