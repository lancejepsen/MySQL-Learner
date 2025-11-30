import os
import sys
import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QMessageBox,
    QSplitter,
)
from PySide6.QtCore import Qt


def resource_path(relative_path: str) -> str:
    """
    Resolve resource paths for PyInstaller EXE or dev environment.
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # ui folder → go up to project root
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.abspath(os.path.join(base, ".."))
    return os.path.join(base, relative_path)


class SandboxBrowser(QWidget):
    """
    A simple table viewer for the SQLite sample.db database.
    Displays all table names and their contents.
    """

    def __init__(self):
        super().__init__()

        self.db_path = resource_path("database/sample.db")

        if not os.path.exists(self.db_path):
            QMessageBox.critical(
                self,
                "Database Missing",
                f"Could not find database:\n{self.db_path}"
            )

        # --- MAIN LAYOUT ---
        layout = QVBoxLayout(self)

        # Splitter (top = table list, bottom = data viewer)
        splitter = QSplitter(Qt.Vertical)

        # Table list (top)
        self.table_list = QListWidget()
        self.table_list.clicked.connect(self.load_table_data)

        # Table contents (bottom)
        self.data_view = QTextEdit()
        self.data_view.setReadOnly(True)

        splitter.addWidget(self.table_list)
        splitter.addWidget(self.data_view)
        splitter.setSizes([200, 1000])

        layout.addWidget(splitter)

        # Load list of tables
        self.load_tables()

    # ----------------------------------------------------------
    # Load all table names from database
    # ----------------------------------------------------------
    def load_tables(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
            )
            tables = [row[0] for row in cur.fetchall()]

            for t in tables:
                self.table_list.addItem(QListWidgetItem(t))

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

    # ----------------------------------------------------------
    # Load selected table data
    # ----------------------------------------------------------
    def load_table_data(self):
        table = self.table_list.currentItem().text()

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(f"SELECT * FROM {table};")
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

            # Build output
            output = f"Table: {table}\n\n"
            output += " | ".join(columns) + "\n"
            output += "-" * 60 + "\n"

            for row in rows:
                row_str = " | ".join(str(v) for v in row)
                output += row_str + "\n"

            self.data_view.setPlainText(output)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Query Error", str(e))

        finally:
            conn.close()
