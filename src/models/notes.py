from collections import UserDict
from typing import List, Optional, Tuple


class Note:
    """Represents a single note containing text and optional tags."""

    def __init__(self, text: str, tags: Optional[List[str]] = None):
        self.text = text
        self.tags = tags if tags is not None else []

    def add_tag(self, tag: str) -> None:
        # Adds a tag only if it doesn't already exist to avoid duplicates
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        # Removes a specific tag, raises a ValueError if not found
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError(f"Tag '{tag}' not found in this note.")

    def __str__(self) -> str:
        # Formats the note for console output
        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        return f"Text: {self.text} | Tags: [{tags_str}]"


class NoteBook(UserDict):
    """Manages a collection of Note objects using unique integer IDs."""

    def __init__(self):
        super().__init__()
        # Internal counter to assign unique, auto-incrementing IDs to new notes
        self.__note_id_counter = 1

    def set_id_counter(self, max_id: int) -> None:
        # Syncs the ID counter after loading existing notes from storage
        self.__note_id_counter = max_id + 1

    def add_note(self, text: str, tags: Optional[List[str]] = None) -> int:
        # Creates a note, assigns an ID, stores it, and returns the ID
        note = Note(text, tags)
        note_id = self.__note_id_counter
        self.data[note_id] = note
        self.__note_id_counter += 1
        return note_id

    def edit_note(self, note_id: int, new_text: str) -> None:
        # Updates the text of an existing note by its ID
        if note_id not in self.data:
            raise ValueError(f"Note with ID {note_id} not found.")
        self.data[note_id].text = new_text

    def delete_note(self, note_id: int) -> None:
        # Removes a note from the dictionary by its ID
        if note_id not in self.data:
            raise ValueError(f"Note with ID {note_id} not found.")
        del self.data[note_id]

    def search_by_text(self, query: str) -> List[Tuple[int, Note]]:
        # Performs a case-insensitive search within note texts
        query_lower = query.lower()
        return [
            (note_id, note) for note_id, note in self.data.items()
            if query_lower in note.text.lower()
        ]

    def search_by_tags(self, search_tags: List[str]) -> List[Tuple[int, Note]]:
        # Finds notes that contain ALL specified tags (case-insensitive subset match)
        search_tags_set = {tag.lower() for tag in search_tags}
        result = []
        for note_id, note in self.data.items():
            note_tags_set = {t.lower() for t in note.tags}
            if search_tags_set.issubset(note_tags_set):
                result.append((note_id, note))
        return result