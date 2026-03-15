def input_error(func):
    """Decorator to catch common input errors and provide context-specific CLI hints."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Provide specific hints for data validation errors (e.g., wrong phone format)
            hints = {
                "add_contact": "👉 Format: add-contact <name>",
                "add_birthday": "👉 Format: add-birthday <name> <DD.MM.YYYY>",
                "add_email": "👉 Format: add-email <name> <email>",
                "add_note": "👉 Format: add-note [text]"
            }
            hint = hints.get(func.__name__, "👉 Type 'help' for command usage.")
            return f"❌ Data error: {e}\n{hint}"
            
        except KeyError:
            # Triggered when searching for a non-existent contact or note ID
            return "❌ Error: Contact or Note not found."
            
        except IndexError:
            # Provide specific hints when required arguments are missing
            hints = {
                "add_contact": "👉 Format: add-contact <name>",
                "add_email": "👉 Format: add-email <name> <email>",
                "add_address": "👉 Format: add-address <name> <address text>",
                "search_contact": "👉 Format: search-contact <query>"
            }
            
            # Auto-generate hints for commands that require exactly one 'name' argument
            if func.__name__ in ["show_contact", "delete_contact", "edit_contact", "remove_field"]:
                hint = f"👉 Format: {func.__name__.replace('_', '-')} <name>"
            else:
                hint = hints.get(func.__name__, "👉 Type 'help' for command usage.")
                
            return f"❌ Error: Argument missing.\n{hint}"
            
    return inner