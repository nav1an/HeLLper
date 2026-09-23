"""Всплывающее окно напоминания"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont


class ReminderPopup(QDialog):
    """Всплывающее окно напоминания по центру экрана"""

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text
        self.on_reschedule = None
        self.on_close = None
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Dialog
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Крестик закрытия в правом верхнем углу
        header_layout = QHBoxLayout()
        header_layout.addStretch()

        self.close_icon_btn = QPushButton("")
        self.close_icon_btn.setFixedSize(30, 30)
        self.close_icon_btn.setCursor(Qt.PointingHandCursor)
        self.close_icon_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                font-size: 16px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.close_icon_btn.clicked.connect(self.close_popup)
        header_layout.addWidget(self.close_icon_btn)

        layout.addLayout(header_layout)

        # Заголовок
        title = QLabel(" Напоминание")
        title.setStyleSheet("""
            color: #0078d4;
            font-size: 18px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текст напоминания
        text_label = QLabel(self.text)
        text_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            padding: 15px;
            background-color: #2b2b2b;
            border-radius: 6px;
        """)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Кнопка "Напомнить позже"
        self.reschedule_btn = QPushButton("Напомнить позже")
        self.reschedule_btn.setCursor(Qt.PointingHandCursor)
        self.reschedule_btn.setFixedHeight(40)
        self.reschedule_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #0078d4;
                border: 1px solid #0078d4;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0078d4;
                color: white;
            }
        """)
        self.reschedule_btn.clicked.connect(self.show_reschedule_dialog)
        buttons_layout.addWidget(self.reschedule_btn)

        # Кнопка "Закрыть" (выполнено)
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setFixedHeight(40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        self.close_btn.clicked.connect(self.close_popup)
        buttons_layout.addWidget(self.close_btn)

        layout.addLayout(buttons_layout)

        self.setFixedSize(400, 250)
        self.center_on_screen()

    def center_on_screen(self):
        """Центрирует окно на экране"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def close_popup(self):
        """Закрывает окно"""
        if self.on_close:
            self.on_close()
        self.accept()

    def show_reschedule_dialog(self):
        """Показывает диалог выбора новой даты/времени"""
        if self.on_reschedule:
            self.on_reschedule()