import os
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from ui.markdown_renderer import MarkdownRenderer


def resource_path(p):
    """EXE-safe path resolver"""
    import sys
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, p)


class CaseStudyViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.renderer = MarkdownRenderer()

        # File locations
        self.questions_md = resource_path("case_study/case_study.md")
        self.answers_md = resource_path("case_study/case_study_answers.md")

        # Split sections
        self.question_blocks = []
        self.answer_blocks = []

        # State
        self.index = 0
        self.show_answers = False

        # =============================================
        # MAIN LAYOUT
        # =============================================
        layout = QVBoxLayout(self)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        layout.addWidget(self.browser)

        # Button bar
        btn_row = QWidget()
        btns = QHBoxLayout(btn_row)
        btns.setContentsMargins(10, 5, 10, 5)

        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.previous_part)

        self.toggle_btn = QPushButton("Show Answer")
        self.toggle_btn.clicked.connect(self.toggle_answer)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_part)

        btns.addWidget(self.prev_btn)
        btns.addWidget(self.toggle_btn)
        btns.addWidget(self.next_btn)

        layout.addWidget(btn_row)

        # Load case study content
        self.load_case_study()
        self.render_part()

    # =============================================
    # LOAD & SPLIT CASE STUDY
    # =============================================
    def load_case_study(self):

        def split_md_file(path):
            if not os.path.exists(path):
                return []

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            # Split at "# <number>."
            parts = re.split(r"(?=^#\s+\d+\.)", text, flags=re.MULTILINE)
            return [p.strip() for p in parts if p.strip()]

        self.question_blocks = split_md_file(self.questions_md)
        self.answer_blocks = split_md_file(self.answers_md)

        # Ensure lengths match
        while len(self.answer_blocks) < len(self.question_blocks):
            self.answer_blocks.append("_No answer available._")

    # =============================================
    # RENDER CURRENT PART
    # =============================================
    def render_part(self):
        question_md = self.question_blocks[self.index]

        if self.show_answers:
            answer_md = self.answer_blocks[self.index]
            combined = question_md + "\n\n## Answer\n\n" + answer_md
            html = self.renderer.render(combined)
        else:
            html = self.renderer.render(question_md)

        self.browser.setHtml(html)

        # Update button states
        self.prev_btn.setEnabled(self.index > 0)
        self.next_btn.setEnabled(self.index < len(self.question_blocks) - 1)

        self.toggle_btn.setText(
            "Hide Answer" if self.show_answers else "Show Answer"
        )

    # =============================================
    # BUTTON ACTIONS
    # =============================================
    def toggle_answer(self):
        self.show_answers = not self.show_answers
        self.render_part()

    def next_part(self):
        if self.index < len(self.question_blocks) - 1:
            self.index += 1
            self.show_answers = False
            self.render_part()

    def previous_part(self):
        if self.index > 0:
            self.index -= 1
            self.show_answers = False
            self.render_part()
