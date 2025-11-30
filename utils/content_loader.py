import os
import sys
import json
from typing import Dict, Any


def resource_path(relative_path: str) -> str:
    """
    Resolves file paths correctly for both:
    - Normal Python execution
    - PyInstaller EXE execution (via _MEIPASS)
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_markdown(path: str) -> str:
    """
    Loads and returns UTF-8 markdown text.
    Raises FileNotFoundError, UnicodeDecodeError, or OSError.
    """
    full_path = resource_path(path)

    with open(full_path, "r", encoding="utf-8") as file:
        return file.read()


def load_quiz(path: str) -> Dict[str, Any]:
    """
    Loads and returns a quiz JSON object.
    Raises FileNotFoundError, UnicodeDecodeError, ValueError, or OSError.
    """
    full_path = resource_path(path)

    with open(full_path, "r", encoding="utf-8") as file:
        return json.load(file)
