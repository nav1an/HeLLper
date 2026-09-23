"""Панель счётчика символов и слов"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QFrame
)
from PySide6.QtCore import Qt


class CharCounterPanel(QWidget):
    """Панель для подсчёта символов, слов и строк"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Заголовок
        title = QLabel("Счётчик символов")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Поле ввода
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Введите или вставьте текст...")
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QTextEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        self.text_input.setFixedHeight(150)
        self.text_input.textChanged.connect(self.update_counter)
        layout.addWidget(self.text_input)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3e3e3e; border: none; margin: 5px 0;")
        layout.addWidget(separator)

        # Статистика
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(10)

        # Символы с пробелами
        self.chars_with_spaces_label = self._create_stat_row("Символы (с пробелами):", "0")
        stats_layout.addWidget(self.chars_with_spaces_label)

        # Символы без пробелов
        self.chars_no_spaces_label = self._create_stat_row("Символы (без пробелов):", "0")
        stats_layout.addWidget(self.chars_no_spaces_label)

        # Слова
        self.words_label = self._create_stat_row("Слова:", "0")
        stats_layout.addWidget(self.words_label)

        # Строки
        self.lines_label = self._create_stat_row("Строки:", "0")
        stats_layout.addWidget(self.lines_label)

        layout.addLayout(stats_layout)
        layout.addStretch()

    def _create_stat_row(self, label_text: str, value_text: str) -> QWidget:
        """Создаёт строку статистики"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)

        label = QLabel(label_text)
        label.setStyleSheet("color: #888; font-size: 13px;")
        layout.addWidget(label)

        layout.addStretch()

        value = QLabel(value_text)
        value.setStyleSheet("""
            color: #0078d4;
            font-size: 14px;
            font-weight: bold;
            min-width: 80px;
            padding: 0 10px;
            text-align: right;
        """)
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(value)

        widget.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-radius: 4px;
            }
        """)

        # Сохраняем ссылку на value для обновления
        widget.value_label = value

        return widget

    def update_counter(self):
        """Обновляет счётчики"""
        import re
        text = self.text_input.toPlainText()

        # Символы с пробелами
        chars_with_spaces = len(text)
        self.chars_with_spaces_label.value_label.setText(str(chars_with_spaces))

        # Символы без пробелов
        chars_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
        self.chars_no_spaces_label.value_label.setText(str(chars_no_spaces))

        # Слова (должны содержать хотя бы одну букву)
        words = len(re.findall(r'\b\w*[a-zA-Zа-яА-ЯёЁ]\w*\b', text))
        self.words_label.value_label.setText(str(words))

        # Строки
        lines = len(text.splitlines()) if text else 0
        self.lines_label.value_label.setText(str(lines))