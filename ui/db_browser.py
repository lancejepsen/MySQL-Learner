import sqlite3
from typing import Optional, List

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QTextBrowser
)

from utils.content_loader import resource_path


class DBBrowser(QWidget):
    """
    Displays available tables in the SQLite database and shows their schema.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.table_list = QListWidget()
        self.viewer = QTextBrowser()

        layout.addWidget(self.table_list)
        layout.addWidget(self.viewer)

        self.conn: Optional[sqlite3.Connection] = None

        self._connect_database()
        self._load_table_list()

        self.table_list.currentTextChanged.connect(self._show_table_info)

    # ----------------------------------------------------------------------
    # Database Initialization
    # ----------------------------------------------------------------------

    def _connect_database(self) -> None:
        """
        Connects to the SQLite database.
        """
        try:
            self.conn = sqlite3.connect(resource_path("database/sample.db"))
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            self.conn = None
            self.viewer.setMarkdown(f"### Database Error\n```\n{e}\n```")

    # ----------------------------------------------------------------------
    # Load Tables
    # ----------------------------------------------------------------------

    def _load_table_list(self) -> None:
        """
        Loads all table names from the SQLite database.
        """
        if not self.conn:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables: List[str] = [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.viewer.setMarkdown(f"### Error Loading Tables\n```\n{e}\n```")
            return

        if not tables:
            self.viewer.setMarkdown("### No tables found in the database.")
            return

        for table in sorted(tables):
            self.table_list.addItem(table)

    # ----------------------------------------------------------------------
    # Display Table Schema
    # ----------------------------------------------------------------------

    def _show_table_info(self, table_name: Optional[str]) -> None:
        """
        Displays column structure and row count for the selected table.
        """
        if not table_name or not self.conn:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
        except sqlite3.Error as e:
            self.viewer.setMarkdown(f"### Error Reading Schema\n```\n{e}\n```")
            return

        if not columns:
            self.viewer.setMarkdown(f"### No columns found for table `{table_name}`.")
            return

        md = f"## Table: {table_name}\n\n"
        md += "| Column | Type |\n|--------|--------|\n"

        for col in columns:
            col_name = col[1]
            col_type = col[2]
            md += f"| {col_name} | {col_type} |\n"

        # Row count
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
        except sqlite3.Error:
            count = "Unknown"

        md += f"\n**Row Count:** {count}"

        self.viewer.setMarkdown(md)
