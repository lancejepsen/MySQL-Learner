import markdown
from pygments import highlight
from pygments.lexers import SqlLexer, TextLexer
from pygments.formatters import HtmlFormatter
import re


class MarkdownRenderer:
    """
    Converts Markdown to HTML with syntax-highlighted SQL blocks.
    """

    def __init__(self):
        self.formatter = HtmlFormatter(style="default", noclasses=False)
        self.css = self.formatter.get_style_defs('.highlight')

        # Regex for fenced code blocks
        self.code_pattern = re.compile(
            r"```(sql|sqlite|mysql)?\n(.*?)```",
            re.DOTALL | re.IGNORECASE
        )

    # -----------------------------------------
    def highlight_code(self, match):
        lang = match.group(1)
        code = match.group(2)

        if lang and lang.lower() in ("sql", "sqlite", "mysql"):
            lexer = SqlLexer()
        else:
            lexer = TextLexer()

        highlighted = highlight(code, lexer, self.formatter)
        return highlighted

    # -----------------------------------------
    def render(self, md_text: str) -> str:
        """
        Convert markdown to HTML with syntax highlighting.
        """

        # Replace code blocks first
        html = self.code_pattern.sub(self.highlight_code, md_text)

        # Convert remaining markdown
        html = markdown.markdown(
            html,
            extensions=["fenced_code", "tables", "toc"]
        )

        # Wrap in HTML/CSS for QTextBrowser
        final_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Segoe UI, Arial, sans-serif;
                    background: #ffffff;
                    color: #333333;
                    padding: 12px;
                    line-height: 1.5em;
                    font-size: 15px;
                }}

                h1, h2, h3 {{
                    font-weight: 600;
                    margin-top: 18px;
                }}

                code {{
                    background: #f1f1f1;
                    padding: 2px 4px;
                    border-radius: 4px;
                    font-size: 14px;
                }}

                pre {{
                    background: #f7f7f7;
                    border: 1px solid #e2e2e2;
                    padding: 10px;
                    border-radius: 6px;
                    overflow-x: auto;
                }}

                {self.css}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

        return final_html
