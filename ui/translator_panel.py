"""Панель переводчика"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox
from PySide6.QtCore import Qt
from config import AVAILABLE_LANGUAGES


class TranslatorPanel(QWidget):
    """Панель переводчика"""

    def __init__(self, translator_service):
        super().__init__()
        self.translator = translator_service
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Выбор языков
        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(10)

        self.lang_from = QComboBox()
        self.lang_from.addItems(list(AVAILABLE_LANGUAGES.keys()))
        self.lang_from.setCurrentIndex(0)

        self.lang_to = QComboBox()
        self.lang_to.addItems(list(AVAILABLE_LANGUAGES.keys()))
        self.lang_to.setCurrentIndex(1)  # По умолчанию Русский

        combo_style = """
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                min-width: 100px;
            }
            QComboBox:hover { border: 1px solid #0078d4; }
            QComboBox::drop-down { border: none; width: 25px; padding-right: 8px; }
            QComboBox::down-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #888;
                margin-top: 2px;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3e3e3e;
                selection-background-color: #0078d4;
                outline: none;
            }
        """

        self.lang_from.setStyleSheet(combo_style)
        self.lang_to.setStyleSheet(combo_style)

        self.swap_btn = QPushButton("🔄")
        self.swap_btn.setFixedSize(36, 36)
        self.swap_btn.setCursor(Qt.PointingHandCursor)
        self.swap_btn.setStyleSheet("""
            QPushButton { 
                background-color: #2b2b2b;
                color: #0078d4; 
                border: 1px solid #3e3e3e;
                border-radius: 6px; 
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #0078d4;
                color: white;
                border: 1px solid #0078d4;
            }
        """)
        self.swap_btn.clicked.connect(self.swap_languages)

        lang_layout.addWidget(self.lang_from)
        lang_layout.addWidget(self.swap_btn)
        lang_layout.addWidget(self.lang_to)

        # Поле ввода
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Введите текст для перевода...")
        self.input_text.setMaximumHeight(100)
        self.input_text.setStyleSheet("""
            QTextEdit { 
                background-color: #2b2b2b; 
                color: white; 
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit:focus { border: 1px solid #0078d4; }
        """)

        # Кнопка перевода
        self.translate_btn = QPushButton("Перевести")
        self.translate_btn.setCursor(Qt.PointingHandCursor)
        self.translate_btn.setStyleSheet("""
            QPushButton { 
                background-color: #0078d4; 
                color: white; 
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1084d8; }
            QPushButton:pressed { background-color: #006cc1; }
            QPushButton:disabled { background-color: #005a9e; color: #888; }
        """)
        self.translate_btn.clicked.connect(self.translate_text)

        # Поле результата
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Перевод появится здесь...")
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(100)
        self.output_text.setStyleSheet("""
            QTextEdit { 
                background-color: #2b2b2b; 
                color: #cccccc; 
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        layout.addLayout(lang_layout)
        layout.addWidget(self.input_text)
        layout.addWidget(self.translate_btn)
        layout.addWidget(self.output_text)
        layout.addStretch()

    def swap_languages(self):
        from_text = self.lang_from.currentText()
        to_text = self.lang_to.currentText()
        self.lang_from.setCurrentText(to_text)
        self.lang_to.setCurrentText(from_text)

    def translate_text(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            return

        self.translate_btn.setText("Перевод...")
        self.translate_btn.setEnabled(False)
        self.output_text.setText("")

        source = self.lang_from.currentText()
        target = self.lang_to.currentText()

        translated, error = self.translator.translate(text, source, target)

        if error:
            self.output_text.setText(f"Ошибка: {error}")
        else:
            self.output_text.setText(translated)

        self.translate_btn.setText("Перевести")
        self.translate_btn.setEnabled(True)