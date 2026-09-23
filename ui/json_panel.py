"""Панель конвертера JSON"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter
from PySide6.QtWidgets import QApplication
import re
from core.json_formatter import JsonFormatterService


class JsonHighlighter(QSyntaxHighlighter):
    """Подсветка синтаксиса JSON"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor(156, 220, 254))

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(206, 145, 120))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(181, 206, 168))

        self.bool_format = QTextCharFormat()
        self.bool_format.setForeground(QColor(86, 156, 214))

        self.null_format = QTextCharFormat()
        self.null_format.setForeground(QColor(200, 200, 200))

    def highlightBlock(self, text):
        for match in re.finditer(r'"([^"]+)"(?=\s*:)', text):
            self.setFormat(match.start(), match.end() - match.start(), self.key_format)

        for match in re.finditer(r'"([^"]*)"', text):
            if not re.match(r'"[^"]*"(?=\s*:)', text[match.start():]):
                self.setFormat(match.start(), match.end() - match.start(), self.string_format)

        for match in re.finditer(r'\b\d+\.?\d*\b', text):
            self.setFormat(match.start(), match.end() - match.start(), self.number_format)

        for match in re.finditer(r'\b(true|false)\b', text):
            self.setFormat(match.start(), match.end() - match.start(), self.bool_format)

        for match in re.finditer(r'\bnull\b', text):
            self.setFormat(match.start(), match.end() - match.start(), self.null_format)


class JsonPanel(QWidget):
    """Панель конвертера JSON"""

    def __init__(self):
        super().__init__()
        self.formatter = JsonFormatterService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Заголовок + выпадающий список отступов
        header_layout = QHBoxLayout()

        title = QLabel("Форматирование JSON")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.indent_combo = QComboBox()
        self.indent_combo.addItems(["2 пробела", "4 пробела", "8 пробелов", "Табуляция"])
        self.indent_combo.setCurrentIndex(1)  # По умолчанию 4 пробела
        self.indent_combo.setFixedWidth(120)
        self.indent_combo.setFixedHeight(28)
        self.indent_combo.setCursor(Qt.PointingHandCursor)
        self.indent_combo.setMaxVisibleItems(4)
        self.indent_combo.setStyleSheet("""
                    QComboBox {
                        background-color: #2b2b2b;
                        color: white;
                        border: 1px solid #3e3e3e;
                        border-radius: 4px;
                        padding: 0 8px;
                        font-size: 11px;
                    }
                    QComboBox:hover {
                        border: 1px solid #0078d4;
                    }
                    QComboBox::drop-down {
                        border: none;
                        width: 20px;
                    }
                    QComboBox::down-arrow {
                        border-left: 4px solid transparent;
                        border-right: 4px solid transparent;
                        border-top: 5px solid #888;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #2b2b2b;
                        color: white;
                        border: 1px solid #3e3e3e;
                        selection-background-color: #0078d4;
                    }
                """)
        header_layout.addWidget(self.indent_combo)

        layout.addLayout(header_layout)

        # Поле ввода
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('{"name": "John", "age": 30}')
        self.input_text.setStyleSheet("""
                    QTextEdit {
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                        border: 1px solid #3e3e3e;
                        border-radius: 6px;
                        padding: 8px;
                        font-family: 'Consolas', 'Courier New', monospace;
                        font-size: 12px;
                    }
                    QTextEdit:focus {
                        border: 1px solid #0078d4;
                    }
                """)
        self.input_text.setFixedHeight(120)
        layout.addWidget(self.input_text)

        # Кнопки: Форматировать + Очистить + Копировать
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self.format_btn = QPushButton("Форматировать")
        self.format_btn.setCursor(Qt.PointingHandCursor)
        self.format_btn.setFixedHeight(32)
        self.format_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0078d4;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 0 20px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1084d8;
                    }
                """)
        self.format_btn.clicked.connect(self.format_json)
        buttons_layout.addWidget(self.format_btn)

        buttons_layout.addStretch()

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setFixedHeight(32)
        self.clear_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2b2b2b;
                        color: #888;
                        border: 1px solid #3e3e3e;
                        border-radius: 4px;
                        padding: 0 20px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #3e3e3e;
                        color: white;
                    }
                """)
        self.clear_btn.clicked.connect(self.clear_all)
        buttons_layout.addWidget(self.clear_btn)

        self.copy_btn = QPushButton("Копировать")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.setFixedHeight(32)
        self.copy_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2b2b2b;
                        color: #0078d4;
                        border: 1px solid #0078d4;
                        border-radius: 4px;
                        padding: 0 20px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #0078d4;
                        color: white;
                    }
                """)
        self.copy_btn.clicked.connect(self.copy_result)
        buttons_layout.addWidget(self.copy_btn)

        layout.addLayout(buttons_layout)

        # Поле вывода
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
                    QTextEdit {
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                        border: 1px solid #3e3e3e;
                        border-radius: 6px;
                        padding: 8px;
                        font-family: 'Consolas', 'Courier New', monospace;
                        font-size: 12px;
                    }
                """)
        self.output_text.setFixedHeight(150)

        self.highlighter = JsonHighlighter(self.output_text.document())
        layout.addWidget(self.output_text)

        layout.addSpacing(10)

    def _get_indent(self):
        """Получить отступ из комбобокса"""
        index = self.indent_combo.currentIndex()
        if index == 0:
            return 2
        elif index == 1:
            return 4
        elif index == 2:
            return 8
        else:
            return "\t"

    def format_json(self):
        raw_text = self.input_text.toPlainText().strip()

        if not raw_text:
            self.output_text.setPlainText("Введите JSON для форматирования")
            return

        indent = self._get_indent()
        formatted, is_valid = self.formatter.format_json(raw_text, indent)
        self.output_text.setPlainText(formatted)

    def copy_result(self):
        text = self.output_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)

            self.copy_btn.setText("✓ Скопировано!")
            self.copy_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #27ae60;
                            color: white;
                            border: 1px solid #27ae60;
                            border-radius: 4px;
                            padding: 0 20px;
                            font-size: 12px;
                        }
                    """)

            QTimer.singleShot(1500, self._reset_copy_button)

    def _reset_copy_button(self):
        self.copy_btn.setText("Копировать")
        self.copy_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2b2b2b;
                        color: #0078d4;
                        border: 1px solid #0078d4;
                        border-radius: 4px;
                        padding: 0 20px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #0078d4;
                        color: white;
                    }
                """)

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()