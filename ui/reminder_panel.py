"""Панель напоминаний"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QScrollArea, QFrame,
    QDateTimeEdit, QTimeEdit
)
from PySide6.QtCore import Qt, QDateTime, QDate, QTime
from core.reminder_service import ReminderService


class ReminderPanel(QWidget):
    """Панель для управления напоминаниями"""

    def __init__(self, reminder_service: ReminderService):
        super().__init__()
        self.reminder_service = reminder_service
        self.init_ui()
        self.refresh_list()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Заголовок
        title = QLabel("Напоминания")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Поле для заметки
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("Введите текст напоминания...")
        self.note_text.setFixedHeight(60)
        self.note_text.setStyleSheet("""
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
        layout.addWidget(self.note_text)

        # Выбор даты и времени
        datetime_layout = QHBoxLayout()
        datetime_layout.setSpacing(8)

        # Календарь (выбор даты)
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFixedHeight(32)
        self.date_edit.setFixedWidth(130)
        self.date_edit.setStyleSheet("""
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
            QDateTimeEdit::drop-down {
                border: none;
                width: 20px;
            }
            QDateTimeEdit::down-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #888;
            }
            QCalendarWidget {
                background-color: #1e1e1e;
                color: white;
                font-size: 11px;
            }
            QCalendarWidget QToolButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #0078d4;
            }
            QCalendarWidget QMenu {
                background-color: #1e1e1e;
                color: white;
            }
            QCalendarWidget QSpinBox {
                background-color: #1e1e1e;
                color: white;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #2b2b2b;
                border: none;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
                background-color: #1e1e1e;
                selection-background-color: #0078d4;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #555;
            }
        """)
        datetime_layout.addWidget(self.date_edit)

        # Время (без секунд) — увеличенные стрелки
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFixedHeight(32)
        self.time_edit.setFixedWidth(110)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 12px;
            }
            QTimeEdit:hover {
                border: 1px solid #0078d4;
            }
            QTimeEdit:focus {
                border: 1px solid #0078d4;
            }
            QTimeEdit::up-button, QTimeEdit::down-button {
                width: 20px;
                height: 15px;
                background-color: #2b2b2b;
                border: none;
                border-radius: 2px;
            }
            QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
                background-color: #0078d4;
            }
            QTimeEdit::up-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 5px solid white;
                width: 0;
                height: 0;
            }
            QTimeEdit::down-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid white;
                width: 0;
                height: 0;
            }
        """)
        datetime_layout.addWidget(self.time_edit)

        datetime_layout.addStretch()

        # Кнопка добавления
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setFixedHeight(32)
        self.add_btn.setStyleSheet("""
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
        self.add_btn.clicked.connect(self.add_reminder)
        datetime_layout.addWidget(self.add_btn)

        layout.addLayout(datetime_layout)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3e3e3e; border: none; margin: 5px 0;")
        layout.addWidget(separator)

        # Заголовок списка
        list_header = QLabel("Активные напоминания:")
        list_header.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(list_header)

        # Список напоминаний с прокруткой
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                background-color: #1e1e1e;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(5, 5, 5, 5)
        self.items_layout.setSpacing(5)
        self.items_layout.addStretch()

        self.scroll_area.setWidget(self.items_container)
        self.scroll_area.setFixedHeight(200)

        layout.addWidget(self.scroll_area)

        # Кнопка очистки выполненных
        clear_layout = QHBoxLayout()
        clear_layout.addStretch()

        self.clear_btn = QPushButton("Очистить выполненные")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setFixedHeight(28)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #888;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
                color: white;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_completed)
        clear_layout.addWidget(self.clear_btn)

        layout.addLayout(clear_layout)

    def add_reminder(self):
        """Добавляет новое напоминание"""
        text = self.note_text.toPlainText().strip()
        if not text:
            return

        # Объединяем дату и время, секунды = 00
        date = self.date_edit.date()
        time = self.time_edit.time()
        combined = QDateTime(date, QTime(time.hour(), time.minute(), 0))
        datetime_str = combined.toString("yyyy-MM-ddTHH:mm:ss")

        self.reminder_service.add_reminder(text, datetime_str)

        # Очищаем поле и ставим время на 5 минут вперёд
        self.note_text.clear()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.time_edit.setTime(QTime.currentTime().addSecs(300))

        self.refresh_list()

    def refresh_list(self):
        """Обновляет список напоминаний"""
        while self.items_layout.count() > 1:
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        reminders = self.reminder_service.get_active_reminders()

        if not reminders:
            empty_label = QLabel("Нет активных напоминаний")
            empty_label.setStyleSheet("color: #666; font-size: 12px; padding: 20px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.items_layout.insertWidget(0, empty_label)
        else:
            for i, reminder in enumerate(reminders):
                widget = self._create_reminder_widget(reminder, i)
                self.items_layout.insertWidget(i, widget)

    def _create_reminder_widget(self, reminder: dict, index: int) -> QWidget:
        """Создаёт виджет для одного напоминания"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        # Текст напоминания
        text = reminder["text"][:80] + "..." if len(reminder["text"]) > 80 else reminder["text"]
        text_label = QLabel(text)
        text_label.setStyleSheet("color: white; font-size: 12px;")
        text_label.setWordWrap(True)
        layout.addWidget(text_label, 1)

        # Дата и время (без секунд)
        try:
            dt = QDateTime.fromString(reminder["datetime"], "yyyy-MM-ddTHH:mm:ss")
            dt_str = dt.toString("dd.MM HH:mm")
        except:
            dt_str = reminder["datetime"][:16]

        dt_label = QLabel(dt_str)
        dt_label.setStyleSheet("color: #888; font-size: 11px; min-width: 60px;")
        layout.addWidget(dt_label)

        # Кнопка удаления
        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888;
                border: none;
                border-radius: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                color: white;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_reminder(index))
        layout.addWidget(delete_btn)

        widget.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
            }
            QWidget:hover {
                background-color: #2a2a2a;
            }
        """)

        return widget

    def delete_reminder(self, index: int):
        """Удаляет напоминание"""
        reminders = self.reminder_service.get_active_reminders()
        if 0 <= index < len(reminders):
            all_reminders = self.reminder_service.get_reminders()
            original_index = all_reminders.index(reminders[index])
            self.reminder_service.remove_reminder(original_index)
            self.refresh_list()

    def clear_completed(self):
        """Очищает выполненные напоминания"""
        self.reminder_service.clear_completed()
        self.refresh_list()