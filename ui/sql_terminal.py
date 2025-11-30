import os
import sys
import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QSplitter,
)
from PySide6.QtCore import Qt


def resource_path(relative_path: str) -> str:
    """
    Return absolute path for resource (EXE-safe).
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # ui folder → go up to root
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.abspath(os.path.join(base, ".."))
    return os.path.join(base, relative_path)


class SQLTerminalViewer(QWidget):   # ⭐ Renamed from SQLTerminal → SQLTerminalViewer
    """
    SQLite-powered SQL terminal.
    Allows users to run SQL against sample.db.
    """

    def __init__(self):
        super().__init__()

        self.db_path = resource_path("database/sample.db")

        # Ensure DB exists
        if not os.path.exists(self.db_path):
            QMessageBox.critical(
                self,
                "Database Missing",
                f"Missing SQLite database:\n{self.db_path}"
            )

        # Main layout
        layout = QVBoxLayout(self)

        # Split vertically (top = query editor, bottom = results)
        splitter = QSplitter(Qt.Vertical)

        # SQL input box
        self.query_edit = QTextEdit()
        self.query_edit.setPlaceholderText(
            "Enter SQL here...\nExample:\nSELECT * FROM employees;"
        )

        # SQL output box
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)

        splitter.addWidget(self.query_edit)
        splitter.addWidget(self.result_display)
        splitter.setSizes([300, 900])  # initial height distribution

        layout.addWidget(splitter)

        # Run button
        self.run_button = QPushButton("Run SQL")
        self.run_button.clicked.connect(self.execute_sql)
        layout.addWidget(self.run_button)

    # ----------------------------------------------------------
    # Execute SQL query against sample.db
    # ----------------------------------------------------------
    def execute_sql(self):
        sql_text = self.query_edit.toPlainText().strip()

        if not sql_text:
            QMessageBox.warning(self, "No Query", "Please enter a SQL query.")
            return

        # Connect to SQLite DB
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
        except sqlite3.Error as e:
            self.result_display.setPlainText(f"Database error:\n{e}")
            return

        # Attempt to run the query
        try:
            cur.execute(sql_text)
            conn.commit()

            # If SELECT query → fetch rows
            if sql_text.lower().startswith("select"):
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

                output = " | ".join(columns) + "\n"
                output += "-" * 60 + "\n"

                for row in rows:
                    row_str = " | ".join(str(v) for v in row)
                    output += row_str + "\n"

                self.result_display.setPlainText(output)
            else:
                # Display message for non-SELECT queries
                self.result_display.setPlainText("Query executed successfully.")

        except sqlite3.Error as e:
            self.result_display.setPlainText(f"SQL Error:\n{e}")

        finally:
            conn.close()
