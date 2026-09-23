"""Панель генератора UUID"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSpinBox, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication
import uuid


class UuidPanel(QWidget):
    """Панель генератора UUID v4"""

    def __init__(self):
        super().__init__()
        self.generated_uuids = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Заголовок
        title = QLabel("Генератор UUID")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Количество + кнопка генерации
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        count_label = QLabel("Количество:")
        count_label.setStyleSheet("color: #888; font-size: 12px;")
        controls_layout.addWidget(count_label)

        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(100)
        self.count_spin.setValue(5)
        self.count_spin.setFixedHeight(32)
        self.count_spin.setFixedWidth(70)
        self.count_spin.setStyleSheet("""
            QSpinBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 12px;
            }
            QSpinBox:hover {
                border: 1px solid #0078d4;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
            }
        """)
        controls_layout.addWidget(self.count_spin)

        controls_layout.addStretch()

        self.generate_btn = QPushButton("Сгенерировать")
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        self.generate_btn.setFixedHeight(32)
        self.generate_btn.setStyleSheet("""
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
        self.generate_btn.clicked.connect(self.generate_uuids)
        controls_layout.addWidget(self.generate_btn)

        layout.addLayout(controls_layout)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3e3e3e; border: none; margin: 5px 0;")
        layout.addWidget(separator)

        # Список UUID с прокруткой
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
        self.items_layout.setSpacing(3)
        self.items_layout.addStretch()

        self.scroll_area.setWidget(self.items_container)
        self.scroll_area.setFixedHeight(250)

        layout.addWidget(self.scroll_area)

        # Кнопка копировать все
        copy_all_layout = QHBoxLayout()
        copy_all_layout.addStretch()

        self.copy_all_btn = QPushButton("Копировать все")
        self.copy_all_btn.setCursor(Qt.PointingHandCursor)
        self.copy_all_btn.setFixedHeight(32)
        self.copy_all_btn.setStyleSheet("""
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
        self.copy_all_btn.clicked.connect(self.copy_all)
        copy_all_layout.addWidget(self.copy_all_btn)

        layout.addLayout(copy_all_layout)

    def generate_uuids(self):
        """Генерирует UUID"""
        count = self.count_spin.value()
        self.generated_uuids = [str(uuid.uuid4()) for _ in range(count)]
        self.refresh_list()

    def refresh_list(self):
        """Обновляет список UUID"""
        while self.items_layout.count() > 1:
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.generated_uuids:
            empty_label = QLabel("Нажмите 'Сгенерировать' для создания UUID")
            empty_label.setStyleSheet("color: #666; font-size: 12px; padding: 20px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.items_layout.insertWidget(0, empty_label)
        else:
            for i, uuid_text in enumerate(self.generated_uuids):
                widget = self._create_uuid_widget(uuid_text)
                self.items_layout.insertWidget(i, widget)

    def _create_uuid_widget(self, uuid_text: str) -> QWidget:
        """Создаёт виджет для одного UUID"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Текст UUID
        uuid_label = QLabel(uuid_text)
        uuid_label.setStyleSheet("""
            color: #d4d4d4;
            font-size: 12px;
            font-family: 'Consolas', 'Courier New', monospace;
        """)
        layout.addWidget(uuid_label, 1)

        # Кнопка копирования (иконка документа)
        copy_btn = QPushButton()
        copy_btn.setFixedSize(28, 28)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }
        """)

        # Рисуем иконку документа
        from PySide6.QtGui import QPainter, QColor, QPen
        from PySide6.QtCore import QRect

        def paint_icon(event):
            painter = QPainter(copy_btn)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor(200, 200, 200), 1.5))
            painter.setBrush(Qt.NoBrush)

            # Прямоугольник документа
            painter.drawRect(QRect(6, 6, 14, 16))
            # Загнутый уголок
            painter.drawLine(QRect(14, 6, 6, 6).topRight(), QRect(14, 6, 6, 6).bottomLeft())
            # Линии текста
            painter.drawLine(9, 12, 17, 12)
            painter.drawLine(9, 15, 17, 15)
            painter.drawLine(9, 18, 15, 18)
            painter.end()

        copy_btn.paintEvent = paint_icon
        copy_btn.clicked.connect(lambda checked, u=uuid_text: self.copy_uuid(u, copy_btn))
        layout.addWidget(copy_btn)

        widget.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-radius: 4px;
            }
            QWidget:hover {
                background-color: #2a2a2a;
            }
        """)

        return widget

    def copy_uuid(self, uuid_text: str, btn: QPushButton):
        """Копирует один UUID"""
        QApplication.clipboard().setText(uuid_text)

        # Визуальная обратная связь
        btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                border: 1px solid #27ae60;
                border-radius: 4px;
            }
        """)
        QTimer.singleShot(800, lambda: btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }
        """))

    def copy_all(self):
        """Копирует все UUID"""
        if self.generated_uuids:
            text = "\n".join(self.generated_uuids)
            QApplication.clipboard().setText(text)

            self.copy_all_btn.setText("✓ Скопировано!")
            self.copy_all_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: 1px solid #27ae60;
                    border-radius: 4px;
                    padding: 0 20px;
                    font-size: 12px;
                }
            """)
            QTimer.singleShot(1500, self._reset_copy_all_btn)

    def _reset_copy_all_btn(self):
        self.copy_all_btn.setText("Копировать все")
        self.copy_all_btn.setStyleSheet("""
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