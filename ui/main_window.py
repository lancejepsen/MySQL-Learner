import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QSizePolicy
)
from PySide6.QtCore import Qt, QTimer

# VIEWERS
from ui.lesson_viewer import LessonViewer
from ui.quiz_viewer import QuizViewer
from ui.practice_mode import PracticeMode
from ui.case_study_viewer import CaseStudyViewer
from ui.sql_terminal import SQLTerminalViewer
from ui.db_browser import DBBrowser     # ⭐ RESTORED


class MainWindow(QMainWindow):
    def __init__(self, app_name="MySQL Learner"):
        super().__init__()

        self.setWindowTitle(app_name + " by Lance Jepsen")

        # -----------------------------------------------
        # CENTRAL WIDGET + LAYOUT
        # -----------------------------------------------
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # -----------------------------------------------
        # TABS
        # -----------------------------------------------
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(False)
        self.tabs.setMovable(False)

        # ORDER OF TABS
        self.tabs.addTab(LessonViewer(), "Lessons")
        self.tabs.addTab(QuizViewer(), "Quizzes")
        self.tabs.addTab(PracticeMode(), "Practice")
        self.tabs.addTab(CaseStudyViewer(), "Case Study")
        self.tabs.addTab(SQLTerminalViewer(), "SQL Terminal")
        self.tabs.addTab(DBBrowser(), "DB Browser")   # ⭐ RESTORED TAB

        layout.addWidget(self.tabs)

        # -----------------------------------------------
        # MAXIMIZATION FIX
        # -----------------------------------------------

        # Remove constraints
        self.setMinimumSize(200, 200)
        self.setMaximumSize(16777215, 16777215)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set screen geometry BEFORE maximizing
        screen = self.get_screen_geometry()
        self.setGeometry(screen)

        # Delay maximize to avoid Win32/Qt race condition
        QTimer.singleShot(150, self.force_maximize)

    # ------------------------------------------------
    # HELPERS
    # ------------------------------------------------
    def get_screen_geometry(self):
        """
        Returns the available geometry of the primary display.
        """
        screen = self.window().screen()
        if screen:
            return screen.availableGeometry()
        else:
            from PySide6.QtGui import QGuiApplication
            return QGuiApplication.primaryScreen().availableGeometry()

    def force_maximize(self):
        """
        Ensures window reliably launches maximized in:
        - Development
        - PyInstaller EXE
        - Inno Setup installation
        """
        try:
            self.showMaximized()
        except Exception:
            geo = self.get_screen_geometry()
            self.setGeometry(geo)
            self.show()
