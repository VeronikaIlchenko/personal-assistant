import difflib
from typing import List, Optional


def suggest_command(user_input: str, available_commands: List[str]) -> Optional[str]:
    """
    Analyzes the user's input and suggests the closest matching command.
    """
    if not user_input or not available_commands:
        return None

    # Find the single closest match with a minimum similarity threshold of 60%
    matches = difflib.get_close_matches(
        word=user_input.lower(),
        possibilities=[cmd.lower() for cmd in available_commands],
        n=1,
        cutoff=0.6
    )

    if matches:
        suggested_lower = matches[0]
        # Return the original case-sensitive command from the available list
        for cmd in available_commands:
            if cmd.lower() == suggested_lower:
                return cmd

    return None


if __name__ == "__main__":
    # Updated test registry matching the actual main.py commands
    COMMANDS = [
        "hello", "help", "add-contact", "show-contact", "all-contacts", 
        "add-birthday", "show-birthdays", "add-email", "add-address", 
        "search-contact", "edit-contact", "remove-field", "delete-contact",
        "add-note", "search-notes", "search-tags", "show-notes", 
        "edit-note", "delete-note", "close", "exit"
    ]

    # Expanded test cases with realistic typos and expected outputs
    test_inputs = {
        "ad-contct": "add-contact",       # Missing letters
        "shw-contact": "show-contact",    # Missing vowel
        "al-contacts": "all-contacts",    # Missing double consonant
        "add-bday": "add-birthday",       # Common abbreviation
        "srch-tags": "search-tags",       # Dropped vowels
        "remve-fild": "remove-field",     # Multiple typos
        "hlp": "help",                    # Dropped vowel
        "exi": "exit",                    # Incomplete word
        "add contact": "add-contact",     # Missing hyphen
        "show notes": "show-notes",       # Missing hyphen
        "qwertyuiop": None,               # Complete gibberish (should return None)
        "del-note": "delete-note"         # Abbreviated
    }

    print("--- Fuzzy Search Testing ---")
    for user_in, expected in test_inputs.items():
        suggestion = suggest_command(user_in, COMMANDS)
        match_status = "✅ PASS" if suggestion == expected else f"❌ FAIL (Expected: {expected})"
        print(f"[{match_status}] Input: '{user_in:<12}' -> Suggested: '{suggestion}'")