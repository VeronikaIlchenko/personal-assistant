import pickle
from pathlib import Path

STORAGE_DIR = Path.home() / "personal_assistant_data"
STORAGE_DIR.mkdir(exist_ok=True)

def save_data(data, filename):
    file_path = STORAGE_DIR / filename
    with open(file_path, "wb") as f:
        pickle.dump(data, f)

def load_data(filename, default_class):
    file_path = STORAGE_DIR / filename
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return default_class()