
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser

from utils.content_loader import load_markdown


class SyllabusViewer(QWidget):
    """
    Displays the course syllabus from syllabus/index.md.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.viewer = QTextBrowser()
        layout.addWidget(self.viewer)

        self._load_syllabus()

    # ----------------------------------------------------------------------

    def _load_syllabus(self) -> None:
        """
        Loads the syllabus markdown or displays an error if not found.
        """
        try:
            text = load_markdown("syllabus/index.md")
            self.viewer.setMarkdown(text)

        except FileNotFoundError:
            self.viewer.setMarkdown(
                "### Syllabus Not Found\n"
                "Create a file at `syllabus/index.md`."
            )

        except UnicodeDecodeError:
            self.viewer.setMarkdown(
                "### Encoding Error\nSyllabus must be UTF-8 encoded."
            )

        except OSError as e:
            self.viewer.setMarkdown(
                f"### Error Reading Syllabus\n```\n{e}\n```"
            )
