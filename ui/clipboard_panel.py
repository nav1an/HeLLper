"""Панель менеджера буфера обмена"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QApplication
)
from PySide6.QtCore import Qt, QTimer, Signal, QEvent
from PySide6.QtGui import QKeyEvent
from core.clipboard import ClipboardService
import pyautogui
import time


class PinIconWidget(QWidget):
    """Виджет с иконкой булавки (эмодзи)"""

    clicked = Signal()

    def __init__(self, is_pinned=False, parent=None):
        super().__init__(parent)
        self._is_pinned = is_pinned

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("🖈" if is_pinned else "🖈")
        self.label.setStyleSheet(self._get_style())
        self.label.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.label)

    def set_pinned(self, is_pinned):
        self._is_pinned = is_pinned
        self.label.setText("🖈" if is_pinned else "")
        self.label.setStyleSheet(self._get_style())

    def _get_style(self):
        if self._is_pinned:
            return """
                font-size: 18px;
                padding: 0;
                margin: 0;
            """
        else:
            return """
                font-size: 18px;
                padding: 0;
                margin: 0;
                opacity: 0.4;
            """

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class ClipboardItemWidget(QWidget):
    """Карточка элемента буфера обмена"""

    item_clicked = Signal(str)
    item_pasted = Signal(str)
    pin_toggled = Signal(int)

    def __init__(self, text: str, is_pinned: bool, index: int, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_pinned = is_pinned
        self.index = index
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        # Текст
        display_text = self.text[:120] + "..." if len(self.text) > 120 else self.text
        display_text = display_text.replace("\n", " ↵ ")

        self.text_label = QLabel(display_text)
        self.text_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            padding: 0;
        """)
        self.text_label.setWordWrap(True)
        self.text_label.setCursor(Qt.PointingHandCursor)
        self.text_label.setToolTip(self.text)
        layout.addWidget(self.text_label, 1)

        # Кнопки действий
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)

        # Кнопка "Вставить"
        self.paste_btn = QPushButton("Вставить")
        self.paste_btn.setCursor(Qt.PointingHandCursor)
        self.paste_btn.setFixedHeight(26)
        self.paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        self.paste_btn.clicked.connect(self._on_paste_clicked)
        buttons_layout.addWidget(self.paste_btn)

        # Кнопка "Копировать"
        self.copy_btn = QPushButton("Копировать")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.setFixedHeight(26)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
                border: 1px solid #555;
            }
        """)
        self.copy_btn.clicked.connect(self._on_copy_clicked)
        buttons_layout.addWidget(self.copy_btn)

        buttons_layout.addStretch()

        # Иконка булавки
        self.pin_icon = PinIconWidget(self.is_pinned)
        self.pin_icon.clicked.connect(self._on_pin_clicked)
        self.pin_icon.setToolTip("Закрепить" if not self.is_pinned else "Открепить")
        buttons_layout.addWidget(self.pin_icon)

        layout.addLayout(buttons_layout)

        self._update_style()

    def _update_style(self):
        if self.is_pinned:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #0078d4;
                    border-radius: 6px;
                }
                QWidget:hover {
                    background-color: #333333;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #252525;
                    border: 1px solid #3e3e3e;
                    border-radius: 6px;
                }
                QWidget:hover {
                    background-color: #2a2a2a;
                    border: 1px solid #555;
                }
            """)

    def _on_copy_clicked(self):
        self.item_clicked.emit(self.text)

    def _on_paste_clicked(self):
        self.item_pasted.emit(self.text)

    def _on_pin_clicked(self):
        self.pin_toggled.emit(self.index)

    def update_pin_state(self, is_pinned: bool):
        self.is_pinned = is_pinned
        self.pin_icon.set_pinned(is_pinned)
        self.pin_icon.setToolTip("Открепить" if is_pinned else "Закрепить")
        self._update_style()


class ClipboardPanel(QWidget):
    """Панель для просмотра и управления буфером обмена"""

    def __init__(self, clipboard_service: ClipboardService):
        super().__init__()
        self.clipboard = clipboard_service
        self.last_clipboard_text = ""
        self.init_ui()
        self.start_monitoring()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(0)

        # Заголовок + кнопка очистки
        header_layout = QHBoxLayout()
        title = QLabel("Менеджер буфера обмена")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.clear_all_btn = QPushButton("Очистить все")
        self.clear_all_btn.setCursor(Qt.PointingHandCursor)
        self.clear_all_btn.setFixedHeight(28)
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
                border: 1px solid #555;
            }
        """)
        self.clear_all_btn.clicked.connect(self.clear_all_history)
        header_layout.addWidget(self.clear_all_btn)

        layout.addLayout(header_layout)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3e3e3e; border: none; margin: 8px 0;")
        layout.addWidget(separator)

        # Список с прокруткой
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
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
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(8)
        self.items_layout.addStretch()

        self.scroll_area.setWidget(self.items_container)
        self.scroll_area.setFixedHeight(300)

        layout.addWidget(self.scroll_area)

        # Отступ между списком и кнопками
        spacer = QWidget()
        spacer.setFixedHeight(15)
        layout.addWidget(spacer)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setFixedHeight(32)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #0078d4;
                border: 1px solid #0078d4;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #0078d4;
                color: white;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_history)
        buttons_layout.addWidget(self.refresh_btn)

        buttons_layout.addStretch()

        self.clear_btn = QPushButton("Очистить не закреплённые")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setFixedHeight(32)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #e67e22;
                border: 1px solid #e67e22;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e67e22;
                color: white;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_history)
        buttons_layout.addWidget(self.clear_btn)

        layout.addLayout(buttons_layout)

    def start_monitoring(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)

    def check_clipboard(self):
        current_text = self.clipboard.get_clipboard_text()
        if current_text and current_text.strip() and current_text != self.last_clipboard_text:
            self.clipboard.add_to_history(current_text)
            self.last_clipboard_text = current_text
            self.refresh_history()

    def refresh_history(self):
        # Очищаем контейнер (оставляем stretch)
        while self.items_layout.count() > 1:
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        history = self.clipboard.get_history()

        # Фильтруем пустые записи
        history = [
            item for item in history
            if isinstance(item, dict) and item.get("text", "").strip()
        ]

        if not history:
            empty_label = QLabel("История пуста")
            empty_label.setStyleSheet("color: #666; font-size: 12px; padding: 20px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.items_layout.insertWidget(0, empty_label)
        else:
            for i, item_data in enumerate(history):
                text = item_data.get("text", "")
                is_pinned = item_data.get("pinned", False)

                widget = ClipboardItemWidget(text, is_pinned, i, self)
                widget.item_clicked.connect(self.on_item_clicked)
                widget.item_pasted.connect(self.on_item_pasted)
                widget.pin_toggled.connect(self.on_pin_toggled)
                self.items_layout.insertWidget(i, widget)

    def on_item_clicked(self, text):
        """Копировать в буфер"""
        self.clipboard.set_clipboard_text(text)
        self.last_clipboard_text = text

    def on_item_pasted(self, text):
        """Копировать и вставить"""
        self.clipboard.set_clipboard_text(text)
        self.last_clipboard_text = text

        # Скрываем окно и эмулируем Ctrl+V
        QTimer.singleShot(100, self._simulate_paste)

    def _simulate_paste(self):
        """Эмулирует нажатие Ctrl+V"""
        # Скрываем главное окно
        self.window().hide()

        # Небольшая задержка перед вставкой
        time.sleep(0.1)

        # Эмулируем Ctrl+V
        pyautogui.hotkey('ctrl', 'v')

        # Показываем окно обратно (с задержкой)
        QTimer.singleShot(500, lambda: self.window().show())

    def on_pin_toggled(self, index):
        self.clipboard.toggle_pin(index)
        self.refresh_history()

    def clear_history(self):
        self.clipboard.clear_history()
        self.last_clipboard_text = self.clipboard.get_clipboard_text()
        self.refresh_history()

    def clear_all_history(self):
        self.clipboard.clear_all_history()
        self.last_clipboard_text = self.clipboard.get_clipboard_text()
        self.refresh_history()