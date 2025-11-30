import os
import re

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QTextBrowser, QSplitter, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from ui.markdown_renderer import MarkdownRenderer


def resource_path(p):
    """Return EXE-safe absolute path."""
    import sys
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base, p)


class LessonViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.renderer = MarkdownRenderer()
        self.lesson_folder = resource_path("lessons")
        self.lesson_files = []   # actual filenames in sorted order
        self.index = 0           # current lesson index

        # ------------------------------------------------------
        # MAIN SPLITTER LAYOUT (left list, right browser)
        # ------------------------------------------------------
        layout = QVBoxLayout(self)

        self.splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(self.splitter)

        # LEFT: Lesson list
        self.list = QListWidget()
        self.list.setMinimumWidth(260)
        self.list.clicked.connect(self.on_list_click)

        # RIGHT: Markdown viewer
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)

        self.splitter.addWidget(self.list)
        self.splitter.addWidget(self.browser)
        self.splitter.setSizes([260, 1500])

        # ------------------------------------------------------
        # NAVIGATION BUTTONS
        # ------------------------------------------------------
        nav_row = QWidget()
        nav_layout = QHBoxLayout(nav_row)
        nav_layout.setContentsMargins(10, 5, 10, 5)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_lesson)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_lesson)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)

        layout.addWidget(nav_row)

        # Load lessons
        self.load_lessons()
        self.render_lesson()

    # ------------------------------------------------------
    # PRETTY PRINTING OF LESSON TITLES
    # lesson_01.md → Lesson 1
    # ------------------------------------------------------
    def pretty_lesson_name(self, filename: str) -> str:
        match = re.search(r"lesson_(\d+)\.md", filename, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            return f"Lesson {num}"
        return filename

    # ------------------------------------------------------
    # LOAD .md FILES FROM /lessons (sorted)
    # ------------------------------------------------------
    def load_lessons(self):
        if not os.path.isdir(self.lesson_folder):
            self.list.addItem("Lessons folder not found.")
            return

        files = sorted(os.listdir(self.lesson_folder))

        for f in files:
            if f.lower().endswith(".md"):
                display = self.pretty_lesson_name(f)

                item = QListWidgetItem(display)
                item.setData(Qt.UserRole, f)  # store real filename
                self.list.addItem(item)

                self.lesson_files.append(f)

    # ------------------------------------------------------
    # LOAD AND RENDER CURRENT LESSON
    # ------------------------------------------------------
    def render_lesson(self):
        if not self.lesson_files:
            self.browser.setText("No lessons found.")
            return

        filename = self.lesson_files[self.index]
        path = os.path.join(self.lesson_folder, filename)

        if not os.path.exists(path):
            self.browser.setText(f"Lesson file missing:\n{path}")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                md = f.read()

            # Convert Markdown → HTML (with SQL highlighting)
            html = self.renderer.render(md)
            self.browser.setHtml(html)

            # Update list highlight
            self.list.setCurrentRow(self.index)

            # Update navigation buttons
            self.prev_button.setEnabled(self.index > 0)
            self.next_button.setEnabled(self.index < len(self.lesson_files) - 1)

        except Exception as e:
            self.browser.setText(f"Error loading lesson:\n{e}")

    # ------------------------------------------------------
    # EVENT: User clicked a lesson in list
    # ------------------------------------------------------
    def on_list_click(self):
        self.index = self.list.currentRow()
        self.render_lesson()

    # ------------------------------------------------------
    # NAV BUTTONS
    # ------------------------------------------------------
    def next_lesson(self):
        if self.index < len(self.lesson_files) - 1:
            self.index += 1
            self.render_lesson()

    def previous_lesson(self):
        if self.index > 0:
            self.index -= 1
            self.render_lesson()
