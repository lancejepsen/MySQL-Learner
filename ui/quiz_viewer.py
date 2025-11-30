import os
import sys
import json

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QTextBrowser, QPushButton, QMessageBox, QSplitter,
    QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt

from ui.markdown_renderer import MarkdownRenderer


def resource_path(p: str) -> str:
    """EXE-safe resource resolver"""
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, p)


class QuizViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Markdown + SQL highlighter
        self.renderer = MarkdownRenderer()

        # Quiz data
        self.quiz_folder = resource_path("quizzes")
        self.quizzes = []
        self.current_index = 0
        self.quiz_answered = 0
        self.quiz_correct = 0

        # ============================================
        # MAIN LAYOUT
        # ============================================
        main_layout = QVBoxLayout(self)

        # ============================================
        # SPLITTER (LEFT LIST, RIGHT MARKDOWN)
        # ============================================
        self.splitter = QSplitter(Qt.Horizontal)

        # LEFT list of questions
        self.list = QListWidget()
        self.list.clicked.connect(self.on_list_clicked)
        self.list.setMinimumWidth(280)

        # RIGHT markdown view
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)

        self.splitter.addWidget(self.list)
        self.splitter.addWidget(self.browser)

        # Preferred widths
        self.splitter.setSizes([300, 1500])

        main_layout.addWidget(self.splitter)

        # ============================================
        # ANSWER BUTTON BAR — MUST HAVE MIN HEIGHT
        # ============================================
        self.button_bar = QWidget()
        self.button_bar.setMinimumHeight(90)
        self.button_bar.setMaximumHeight(120)
        self.button_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.button_layout = QHBoxLayout(self.button_bar)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.setSpacing(20)

        main_layout.addWidget(self.button_bar)
        self.answer_buttons = []

        # ============================================
        # NAVIGATION BAR
        # ============================================
        self.nav_bar = QWidget()
        self.nav_bar.setMinimumHeight(60)
        self.nav_bar.setMaximumHeight(75)

        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(10, 5, 10, 5)
        nav_layout.setSpacing(20)

        self.prev_button = QPushButton("Previous")
        self.prev_button.setMinimumHeight(40)
        self.prev_button.clicked.connect(self.previous_question)

        self.next_button = QPushButton("Next")
        self.next_button.setMinimumHeight(40)
        self.next_button.clicked.connect(self.next_question)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)

        main_layout.addWidget(self.nav_bar)

        # ============================================
        # SCORE LABEL + RESET BUTTON
        # ============================================
        score_row = QWidget()
        score_layout = QHBoxLayout(score_row)
        score_layout.setContentsMargins(10, 5, 10, 5)
        score_layout.setSpacing(20)

        self.quiz_score_label = QLabel("Quiz Score: 0/0 (0%)")
        self.quiz_score_label.setAlignment(Qt.AlignCenter)
        self.quiz_score_label.setStyleSheet(
            "font-size: 14px; font-weight: bold;"
        )

        self.reset_button = QPushButton("Clear Quiz Score")
        self.reset_button.setMinimumHeight(35)
        self.reset_button.clicked.connect(self.reset_quiz_score)

        score_layout.addWidget(self.quiz_score_label)
        score_layout.addWidget(self.reset_button)

        main_layout.addWidget(score_row)

        # ============================================
        # STRETCH PRIORITIES — CRITICAL FIX
        # ============================================
        main_layout.setStretch(0, 10)  # splitter
        main_layout.setStretch(1, 1)   # answer buttons
        main_layout.setStretch(2, 1)   # nav bar
        main_layout.setStretch(3, 0)   # score bar

        # ============================================
        # LOAD DATA & FIRST QUESTION
        # ============================================
        self.load_quizzes()
        self.load_question()

    # ======================================================
    # LOAD QUIZ FILES
    # ======================================================
    def load_quizzes(self):
        if not os.path.isdir(self.quiz_folder):
            self.list.addItem("Quizzes folder not found.")
            return

        for filename in sorted(os.listdir(self.quiz_folder)):
            if filename.lower().endswith(".json"):
                fpath = os.path.join(self.quiz_folder, filename)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    quiz = {
                        "question": data["question"],
                        "answers": data["answers"],
                        "correct": data["correct"]
                    }

                    self.quizzes.append(quiz)
                    self.list.addItem(
                        QListWidgetItem(quiz["question"][:60])
                    )
                except Exception as e:
                    print("Error loading quiz:", e)

    # ======================================================
    # LOAD QUESTION
    # ======================================================
    def load_question(self):
        if not self.quizzes:
            return

        quiz = self.quizzes[self.current_index]

        # Convert question to Markdown → HTML
        md = f"# Question {self.current_index + 1}\n\n{quiz['question']}"
        html = self.renderer.render(md)
        self.browser.setHtml(html)

        # Create answer buttons
        self.create_answer_buttons(quiz["answers"])

        # Update score
        self.list.setCurrentRow(self.current_index)
        self.update_score()

    # ======================================================
    # LIST CLICK
    # ======================================================
    def on_list_clicked(self):
        self.current_index = self.list.currentRow()
        self.load_question()

    # ======================================================
    # NAVIGATION
    # ======================================================
    def next_question(self):
        if self.current_index < len(self.quizzes) - 1:
            self.current_index += 1
            self.load_question()

    def previous_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()

    # ======================================================
    # CREATE ANSWER BUTTONS
    # ======================================================
    def create_answer_buttons(self, answers):
        for btn in self.answer_buttons:
            self.button_layout.removeWidget(btn)
            btn.deleteLater()
        self.answer_buttons.clear()

        for i, text in enumerate(answers):
            letter = chr(65 + i)
            btn = QPushButton(f"{letter}. {text}")
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda _, g=letter: self.check_answer(g))
            self.button_layout.addWidget(btn)
            self.answer_buttons.append(btn)

    # ======================================================
    # ANSWER CHECKING
    # ======================================================
    def check_answer(self, guess):
        correct_letter = chr(65 + self.quizzes[self.current_index]["correct"])

        self.quiz_answered += 1
        if guess == correct_letter:
            self.quiz_correct += 1
            QMessageBox.information(self, "Correct!", f"{guess} is correct!")
        else:
            QMessageBox.warning(
                self,
                "Incorrect",
                f"{guess} is incorrect.\n\nCorrect answer: {correct_letter}"
            )

        self.update_score()

    # ======================================================
    # SCORE UPDATE
    # ======================================================
    def update_score(self):
        if self.quiz_answered == 0:
            pct = 0
        else:
            pct = int(self.quiz_correct / self.quiz_answered * 100)

        self.quiz_score_label.setText(
            f"Quiz Score: {self.quiz_correct}/{self.quiz_answered} ({pct}%)"
        )

    # ======================================================
    # CLEAR SCORE BUTTON
    # ======================================================
    def reset_quiz_score(self):
        self.quiz_answered = 0
        self.quiz_correct = 0
        self.update_score()
        QMessageBox.information(self, "Score Reset", "Quiz score has been cleared.")
