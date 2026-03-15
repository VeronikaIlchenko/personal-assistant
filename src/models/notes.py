from collections import UserDict
from typing import List, Optional, Tuple


class Note:
    """Клас для зберігання окремої нотатки та її тегів."""

    def __init__(self, text: str, tags: Optional[List[str]] = None):
        self.text = text
        self.tags = tags if tags is not None else []

    def add_tag(self, tag: str) -> None:
        """Додає тег до нотатки, якщо його ще немає."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Видаляє тег з нотатки."""
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError(f"Тег '{tag}' не знайдено у цій нотатці.")

    def __str__(self) -> str:
        """Форматований вивід нотатки."""
        tags_str = ", ".join(self.tags) if self.tags else "Немає тегів"
        return f"Текст: {self.text} | Теги: [{tags_str}]"


class NoteBook(UserDict):
    """Клас для управління списком нотаток."""

    def __init__(self):
        super().__init__()
        self.__note_id_counter = 1

    def set_id_counter(self, max_id: int) -> None:
        """
        Встановлює значення лічильника ID.
        Критично важливо викликати цей метод після завантаження даних з диска.
        """
        self.__note_id_counter = max_id + 1

    def add_note(self, text: str, tags: Optional[List[str]] = None) -> int:
        """Створює нотатку, зберігає її і повертає унікальний ID."""
        note = Note(text, tags)
        note_id = self.__note_id_counter
        self.data[note_id] = note
        self.__note_id_counter += 1
        return note_id

    def edit_note(self, note_id: int, new_text: str) -> None:
        """Змінює текст існуючої нотатки за ID."""
        if note_id not in self.data:
            raise ValueError(f"Нотатку з ID {note_id} не знайдено.")
        self.data[note_id].text = new_text

    def delete_note(self, note_id: int) -> None:
        """Видаляє нотатку за ID."""
        if note_id not in self.data:
            raise ValueError(f"Нотатку з ID {note_id} не знайдено.")
        del self.data[note_id]

    def search_by_text(self, query: str) -> List[Tuple[int, Note]]:
        """Шукає нотатки за текстом."""
        query_lower = query.lower()
        return [
            (note_id, note) for note_id, note in self.data.items()
            if query_lower in note.text.lower()
        ]

    def search_by_tags(self, search_tags: List[str]) -> List[Tuple[int, Note]]:
        """Шукає нотатки, які містять УСІ задані теги."""
        search_tags_set = {tag.lower() for tag in search_tags}
        result = []
        for note_id, note in self.data.items():
            note_tags_set = {t.lower() for t in note.tags}
            if search_tags_set.issubset(note_tags_set):
                result.append((note_id, note))
        return result