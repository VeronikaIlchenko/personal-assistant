from setuptools import setup, find_packages

setup(
    name="personal-assistant",
    version="1.0.0",
    description="A powerful Command Line Interface (CLI) application for managing contacts and notes.",
    author="Veronika, Alisa, Yaroslav",
    
    # Map the root package to the 'src' directory
    package_dir={"": "src"},
    
    # Automatically discover all packages (folders with __init__.py like models, utils) inside 'src'
    packages=find_packages(where="src"),
    
    # Specify standalone modules located directly in 'src'
    py_modules=["main", "storage"],
    
    # Define the global CLI command 'assistant' that triggers the main() function in main.py
    entry_points={
        "console_scripts": [
            "assistant=main:main",
        ]
    },
    
    # List of external dependencies (empty as we only use built-in Python libraries)
    install_requires=[],
    
    # Specify the minimum Python version required
    python_requires=">=3.8",
)