from setuptools import setup, find_packages

setup(
    name="personal-assistant",
    version="1.0.0",
    description="A powerful Command Line Interface (CLI) application for managing contacts and notes.",
    author="Veronika, Alisa, Yaroslav",
    # Вказуємо, що весь наш вихідний код лежить у папці src
    package_dir={"": "src"},
    # Знаходимо всі пакети (папки з __init__.py, такі як models та utils)
    packages=find_packages(where="src"),
    # Вказуємо окремі файли, які лежать прямо в src
    py_modules=["main", "storage"],
    # Найголовніше: створюємо консольну команду "assistant", яка запустить функцію main() з файлу main.py
    entry_points={
        "console_scripts": [
            "assistant=main:main",
        ]
    },
    install_requires=[
    ],
    python_requires=">=3.8",
)