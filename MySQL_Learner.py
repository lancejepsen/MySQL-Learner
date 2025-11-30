import sys
import os
import sqlite3
import logging

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow


# ============================================================
# EXE-SAFE RESOURCE PATH
# ============================================================
def resource_path(relative_path: str) -> str:
    """
    Return absolute path – works for PyInstaller EXE and normal Python.
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, relative_path)


# ============================================================
# SAFE LOGGING LOCATION (LOCALAPPDATA)
# ============================================================
def setup_logging():
    local_appdata = os.getenv("LOCALAPPDATA", "")
    log_dir = os.path.join(local_appdata, "MySQL_Learner")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, "mysql_learner.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Application started.")
    logging.info(f"Logging to: {log_path}")


# ============================================================
# DATABASE INITIALIZATION (SQLite)
# ============================================================
def ensure_database_exists():
    """
    Ensures /database/sample.db exists.
    Creates it using /database/init.sql if missing.
    """

    # Where the EXE/runtime is located
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    db_dir = os.path.join(base_dir, "database")
    db_path = os.path.join(db_dir, "sample.db")
    init_sql_path = resource_path("database/init.sql")

    os.makedirs(db_dir, exist_ok=True)

    if os.path.exists(db_path):
        logging.info(f"Database found: {db_path}")
        return

    logging.info("Database missing — creating new SQLite DB...")
    logging.info(f"Using init SQL at: {init_sql_path}")

    try:
        with open(init_sql_path, "r", encoding="utf-8") as f:
            script = f.read()

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.executescript(script)
        conn.commit()
        conn.close()

        logging.info(f"Database created successfully at: {db_path}")

    except Exception as e:
        logging.error(f"Database creation error: {e}")


# ============================================================
# MAIN APPLICATION ENTRY
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    setup_logging()
    ensure_database_exists()

    window = MainWindow(app_name="MySQL Learner")

    # IMPORTANT:
    # Do NOT maximize here.
    # main_window.py will control geometry and maximization.
    window.show()

    sys.exit(app.exec())
