import os
import json
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QTextBrowser, QSplitter, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from ui.markdown_renderer import MarkdownRenderer


def resource_path(p):
    """EXE-safe path resolver."""
    import sys
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, p)


class PracticeMode(QWidget):
    def __init__(self):
        super().__init__()

        self.renderer = MarkdownRenderer()
        self.folder = resource_path("practice")

        # Cached content
        self.last_question = ""
        self.last_mysql = ""
        self.last_sqlite = ""
        self.showing_answer = False

        # =====================================================
        # MAIN SPLITTER LAYOUT
        # =====================================================
        layout = QVBoxLayout(self)

        self.splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(self.splitter)

        # LEFT LIST
        self.list = QListWidget()
        self.list.setMinimumWidth(260)
        self.list.clicked.connect(self.load_item)

        # RIGHT MARKDOWN VIEWER
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)

        self.splitter.addWidget(self.list)
        self.splitter.addWidget(self.browser)
        self.splitter.setSizes([260, 1500])

        # =====================================================
        # SHOW/HIDE ANSWER BUTTON
        # =====================================================
        self.button_row = QWidget()
        btn_layout = QHBoxLayout(self.button_row)
        btn_layout.setContentsMargins(10, 5, 10, 5)

        self.answer_button = QPushButton("Show Answer")
        self.answer_button.setMinimumHeight(40)
        self.answer_button.clicked.connect(self.toggle_answer)

        btn_layout.addWidget(self.answer_button)
        layout.addWidget(self.button_row)

        # Load practice items
        self.populate()

    # =====================================================
    # PRETTY NAME CONVERSION (problem_01.json → Problem 1)
    # =====================================================
    def pretty_problem_name(self, filename: str) -> str:
        match = re.search(r"problem_(\d+)\.json", filename, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            return f"Problem {num}"
        return filename

    # =====================================================
    # LOAD PRACTICE FILE LIST
    # =====================================================
    def populate(self):
        if not os.path.isdir(self.folder):
            self.list.addItem("No 'practice' folder found.")
            return

        files = sorted(os.listdir(self.folder))

        for f in files:
            if f.lower().endswith(".json"):
                display_name = self.pretty_problem_name(f)

                item = QListWidgetItem(display_name)
                item.setData(Qt.UserRole, f)  # store real filename

                self.list.addItem(item)

        if self.list.count() == 0:
            self.list.addItem("No JSON practice files found.")

    # =====================================================
    # LOAD SELECTED PRACTICE PROBLEM
    # =====================================================
    def load_item(self):
        item = self.list.currentItem()
        if not item:
            return

        filename = item.data(Qt.UserRole)   # load actual filename
        path = os.path.join(self.folder, filename)

        if not os.path.exists(path):
            self.browser.setText("File not found.")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Cache contents for toggle behavior
            self.last_question = data.get("question", "")
            self.last_mysql = data.get("mysql_example", "")
            self.last_sqlite = data.get("sqlite_example", "")

            # Reset state
            self.showing_answer = False
            self.answer_button.setText("Show Answer")

            # Question only
            md = f"# Practice Problem\n\n{self.last_question}"
            html = self.renderer.render(md)
            self.browser.setHtml(html)

        except Exception as e:
            self.browser.setText(f"Error loading file:\n{e}")

    # =====================================================
    # SHOW / HIDE ANSWER TOGGLE
    # =====================================================
    def toggle_answer(self):
        if not self.last_question:
            return

        if self.showing_answer:
            # Hide answers → show question only
            self.showing_answer = False
            self.answer_button.setText("Show Answer")

            md = f"# Practice Problem\n\n{self.last_question}"
            html = self.renderer.render(md)
            self.browser.setHtml(html)

        else:
            # Show SQL answers
            self.showing_answer = True
            self.answer_button.setText("Hide Answer")

            md = f"# Practice Problem\n\n{self.last_question}\n\n"

            if self.last_mysql:
                md += "## MySQL Version\n```sql\n" + self.last_mysql.strip() + "\n```\n\n"

            if self.last_sqlite:
                md += "## SQLite Version\n```sql\n" + self.last_sqlite.strip() + "\n```\n"

            html = self.renderer.render(md)
            self.browser.setHtml(html)
