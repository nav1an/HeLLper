"""Диалог переноса напоминания"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QDateTimeEdit
)
from PySide6.QtCore import Qt, QDateTime


class RescheduleDialog(QDialog):
    """Диалог выбора новой даты и времени для напоминания"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_datetime = None
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Dialog
        )
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Напомнить позже")
        title.setStyleSheet("""
            color: #0078d4;
            font-size: 16px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Быстрые кнопки
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(8)

        for minutes, label in [(5, "5 мин"), (15, "15 мин"), (30, "30 мин"), (60, "1 час")]:
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2b2b2b;
                    color: white;
                    border: 1px solid #3e3e3e;
                    border-radius: 4px;
                    padding: 0 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #0078d4;
                    border: 1px solid #0078d4;
                }
            """)
            btn.clicked.connect(lambda checked, m=minutes: self.quick_reschedule(m))
            quick_layout.addWidget(btn)

        layout.addLayout(quick_layout)

        # Разделитель
        from PySide6.QtWidgets import QFrame
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3e3e3e; border: none;")
        layout.addWidget(separator)

        # Выбор даты и времени
        datetime_label = QLabel("Или выберите дату и время:")
        datetime_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(datetime_label)

        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(300))
        self.datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setFixedHeight(35)
        self.datetime_edit.setStyleSheet("""
            QDateTimeEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 12px;
            }
            QDateTimeEdit:hover {
                border: 1px solid #0078d4;
            }
        """)
        layout.addWidget(self.datetime_edit)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setFixedHeight(35)
        self.cancel_btn.setStyleSheet("""
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
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        buttons_layout.addStretch()

        self.confirm_btn = QPushButton("Подтвердить")
        self.confirm_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_btn.setFixedHeight(35)
        self.confirm_btn.setStyleSheet("""
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
        self.confirm_btn.clicked.connect(self.confirm_reschedule)
        buttons_layout.addWidget(self.confirm_btn)

        layout.addLayout(buttons_layout)

        self.setFixedSize(350, 280)
        self.center_on_screen()

    def center_on_screen(self):
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def quick_reschedule(self, minutes: int):
        """Быстрый перенос на N минут"""
        from PySide6.QtCore import QDateTime
        self.selected_datetime = QDateTime.currentDateTime().addSecs(minutes * 60)
        self.accept()

    def confirm_reschedule(self):
        """Подтверждение выбранной даты/времени"""
        self.selected_datetime = self.datetime_edit.dateTime()
        self.accept()

    def get_selected_datetime(self):
        """Возвращает выбранную дату и время"""
        return self.selected_datetime