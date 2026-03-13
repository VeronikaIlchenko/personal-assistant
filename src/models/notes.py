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
        """Видаляє тег з нотатки. Викидає ValueError, якщо тег не знайдено."""
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError(f"Тег '{tag}' не знайдено у цій нотатці.")

    def __str__(self) -> str:
        """Форматований вивід нотатки."""
        tags_str = ", ".join(self.tags) if self.tags else "Немає тегів"
        return f"Текст: {self.text} | Теги: [{tags_str}]"


class NoteBook(UserDict):
    """Клас для управління списком нотаток. Зберігає нотатки у вигляді {note_id: Note}."""

    def __init__(self):
        super().__init__()
        self.__note_id_counter = 1  # Приватний лічильник для унікальних ID нотаток

    def add_note(self, text: str, tags: Optional[List[str]] = None) -> int:
        """Створює нотатку, зберігає її і повертає унікальний ID."""
        note = Note(text, tags)
        note_id = self.__note_id_counter
        self.data[note_id] = note
        self.__note_id_counter += 1
        return note_id

    def edit_note(self, note_id: int, new_text: str) -> None:
        """Змінює текст існуючої нотатки за ID. Викидає ValueError, якщо ID не знайдено."""
        if note_id not in self.data:
            raise ValueError(f"Нотатку з ID {note_id} не знайдено.")
        self.data[note_id].text = new_text

    def delete_note(self, note_id: int) -> None:
        """Видаляє нотатку за ID. Викидає ValueError, якщо ID не знайдено."""
        if note_id not in self.data:
            raise ValueError(f"Нотатку з ID {note_id} не знайдено.")
        del self.data[note_id]

    def search_by_text(self, query: str) -> List[Tuple[int, Note]]:
        """Шукає нотатки, що містять заданий текст. Повертає список пар (note_id, Note)."""
        query_lower = query.lower()
        return [
            (note_id, note) for note_id, note in self.data.items()
            if query_lower in note.text.lower()
        ]

    def search_by_tags(self, search_tags: List[str]) -> List[Tuple[int, Note]]:
        """Шукає нотатки, які містять УСІ задані теги зі списку."""
        search_tags_lower = [tag.lower() for tag in search_tags]
        result = []
        for note_id, note in self.data.items():
            note_tags_lower = [t.lower() for t in note.tags]
            if all(tag in note_tags_lower for tag in search_tags_lower):
                result.append((note_id, note))
        return result


if __name__ == "__main__":
    # Базове тестування функціоналу
    notebook = NoteBook()

    id1 = notebook.add_note("Купити молоко та хліб", ["покупки", "їжа"])
    id2 = notebook.add_note("Зателефонувати мамі ввечері", ["сім'я"])
    id3 = notebook.add_note("Підготувати звіт для роботи", ["робота", "важливе"])

    print("--- Всі нотатки ---")
    for n_id, n in notebook.data.items():
        print(f"ID {n_id}: {n}")

    notebook.edit_note(id1, "Купити молоко, хліб та каву")
    notebook.data[id1].add_tag("кава")
    
    print("\n--- Після редагування ID 1 ---")
    print(f"ID {id1}: {notebook.data[id1]}")

    print("\n--- Пошук за текстом 'робот' ---")
    for n_id, n in notebook.search_by_text("робот"):
        print(f"ID {n_id}: {n}")

    print("\n--- Пошук за ДЕКІЛЬКОМА тегами ['робота', 'важливе'] ---")
    for n_id, n in notebook.search_by_tags(["робота", "важливе"]):
        print(f"ID {n_id}: {n}")

    print("\n--- Спроба видалити неіснуючу нотатку ---")
    try:
        notebook.delete_note(99)
    except ValueError as e:
        print(f"Спіймано помилку: {e}")