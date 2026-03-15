import pickle
from pathlib import Path

# Define a dedicated storage directory in the user's home folder
# exist_ok=True ensures the folder is created only if it doesn't already exist
STORAGE_DIR = Path.home() / ".personal_assistant_data"
STORAGE_DIR.mkdir(exist_ok=True)

def save_data(data, filename):
    """Serializes and saves the application data to a binary file."""
    file_path = STORAGE_DIR / filename
    with open(file_path, "wb") as f:
        pickle.dump(data, f)

def load_data(filename, default_class):
    """
    Loads and deserializes data from a binary file.
    Returns a new instance of default_class if the file is missing or corrupted.
    """
    file_path = STORAGE_DIR / filename
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        # Fallback to an empty AddressBook or NoteBook if loading fails
        return default_class()