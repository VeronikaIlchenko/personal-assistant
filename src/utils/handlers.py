def input_error(func):
    """Декоратор для перехоплення типових помилок введення та виводу підказок."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Оновлені підказки відповідно до нового UX
            hints = {
                "add_contact": "👉 Format: add-contact <name>",
                "add_birthday": "👉 Format: add-birthday <name> <DD.MM.YYYY>",
                "add_email": "👉 Format: add-email <name> <email>",
                "add_note": "👉 Format: add-note [text]"
            }
            hint = hints.get(func.__name__, "👉 Type 'help' for command usage.")
            return f"❌ Data error: {e}\n{hint}"
            
        except KeyError:
            return "❌ Error: Contact or Note not found."
            
        except IndexError:
            # Оновлені підказки для відсутніх аргументів
            hints = {
                "add_contact": "👉 Format: add-contact <name>",
                "add_email": "👉 Format: add-email <name> <email>",
                "add_address": "👉 Format: add-address <name> <address text>",
                "search_contact": "👉 Format: search-contact <query>"
            }
            
            # Якщо функція працює тільки з ім'ям, генеруємо підказку автоматично
            if func.__name__ in ["show_contact", "delete_contact", "edit_contact", "remove_field"]:
                hint = f"👉 Format: {func.__name__.replace('_', '-')} <name>"
            else:
                hint = hints.get(func.__name__, "👉 Type 'help' for command usage.")
                
            return f"❌ Error: Argument missing.\n{hint}"
            
    return inner