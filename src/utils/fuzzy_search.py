import difflib
from typing import List, Optional


def suggest_command(user_input: str, available_commands: List[str]) -> Optional[str]:
    """
    Аналізує введений користувачем текст і пропонує найбільш схожу команду.
    
    :param user_input: Рядок, який ввів користувач (наприклад, з опечаткою).
    :param available_commands: Список доступних правильних команд.
    :return: Найбільш схожа команда або None, якщо збігів не знайдено.
    """
    if not user_input or not available_commands:
        return None

    # Шукаємо 1 найближчий збіг із порогом схожості 60%
    matches = difflib.get_close_matches(
        word=user_input.lower(),
        possibilities=[cmd.lower() for cmd in available_commands],
        n=1,
        cutoff=0.6
    )

    if matches:
        suggested_lower = matches[0]
        for cmd in available_commands:
            if cmd.lower() == suggested_lower:
                return cmd

    return None


if __name__ == "__main__":
    COMMANDS = [
        "add", "delete", "edit", "search", 
        "show all", "help", "exit", "close",
        "add-note", "delete-note"
    ]

    test_inputs = [
        "ad",          # очікуємо 'add'
        "delte",       # очікуємо 'delete'
        "edti",        # очікуємо 'edit'
        "shw al",      # очікуємо 'show all'
        "asdfgh",      # очікуємо None (повна маячня)
        "add-nto"      # очікуємо 'add-note'
    ]

    print("--- Тестування Fuzzy Search ---")
    for user_in in test_inputs:
        suggestion = suggest_command(user_in, COMMANDS)
        if suggestion:
            print(f"Введено: '{user_in}' -> Можливо, ви мали на увазі: '{suggestion}'?")
        else:
            print(f"Введено: '{user_in}' -> Збігів не знайдено.")