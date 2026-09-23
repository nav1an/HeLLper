"""Генератор валидных номеров банковских карт"""
import random
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QCursor, QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication


class CardGeneratorPanel(QWidget):
    """Панель генератора банковских карт"""

    def __init__(self):
        super().__init__()
        self.generated_cards = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Заголовок
        title = QLabel("Генератор карт")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Выбор системы + количество + кнопка
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        # Выбор платёжной системы
        self.system_combo = QComboBox()
        self.system_combo.setCursor(Qt.PointingHandCursor)
        self.system_combo.setFixedHeight(32)
        self.system_combo.setFixedWidth(140)
        self.system_combo.addItems(["МИР", "Visa", "MasterCard"])
        self.system_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 12px;
            }
            QComboBox:hover { border: 1px solid #0078d4; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox::down-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #888;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3e3e3e;
                selection-background-color: #0078d4;
            }
        """)
        controls_layout.addWidget(self.system_combo)

        # Количество
        count_label = QLabel("Кол-во:")
        count_label.setStyleSheet("color: #888; font-size: 12px;")
        controls_layout.addWidget(count_label)

        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(50)
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
            QSpinBox:hover { border: 1px solid #0078d4; }
            QSpinBox::up-button, QSpinBox::down-button { width: 16px; }
        """)
        controls_layout.addWidget(self.count_spin)

        controls_layout.addStretch()

        # Кнопка генерации
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
            QPushButton:hover { background-color: #1084d8; }
        """)
        self.generate_btn.clicked.connect(self.generate_cards)
        controls_layout.addWidget(self.generate_btn)

        layout.addLayout(controls_layout)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3e3e3e; border: none; margin: 5px 0;")
        layout.addWidget(separator)

        # Список карт
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
                border: none; background: transparent; width: 6px; margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #555; min-height: 20px; border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover { background: #777; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
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
        copy_layout = QHBoxLayout()
        copy_layout.addStretch()

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
            QPushButton:hover { background-color: #0078d4; color: white; }
        """)
        self.copy_all_btn.clicked.connect(self.copy_all)
        copy_layout.addWidget(self.copy_all_btn)

        layout.addLayout(copy_layout)

    def _luhn_checksum(self, number: str) -> int:
        """Вычисляет контрольную цифру по алгоритму Луна"""
        digits = [int(d) for d in number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for d in even_digits:
            total += sum(divmod(d * 2, 10))
        return (10 - (total % 10)) % 10

    def _generate_card_number(self, system: str) -> str:
        """Генерирует валидный номер карты"""
        prefixes = {
            "МИР": [f"220{i}" for i in range(0, 5)],
            "Visa": ["4"],
            "MasterCard": [f"{i}" for i in range(51, 56)] + [f"{i}" for i in range(2221, 2230)]
        }

        prefix = random.choice(prefixes[system])
        remaining_length = 16 - len(prefix) - 1
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])

        base_number = prefix + random_part
        check_digit = self._luhn_checksum(base_number + "0")

        return base_number + str(check_digit)

    def _format_card_number(self, number: str) -> str:
        """Форматирует номер карты группами по 4 цифры"""
        return ' '.join([number[i:i+4] for i in range(0, 16, 4)])

    def generate_cards(self):
        """Генерирует карты"""
        system = self.system_combo.currentText()
        count = self.count_spin.value()
        self.generated_cards = [self._generate_card_number(system) for _ in range(count)]
        self.refresh_list()

    def refresh_list(self):
        """Обновляет список карт"""
        while self.items_layout.count() > 1:
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.generated_cards:
            empty_label = QLabel("Нажмите 'Сгенерировать' для создания карт")
            empty_label.setStyleSheet("color: #666; font-size: 12px; padding: 20px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.items_layout.insertWidget(0, empty_label)
        else:
            for i, card_number in enumerate(self.generated_cards):
                widget = self._create_card_widget(card_number)
                self.items_layout.insertWidget(i, widget)

    def _create_card_widget(self, card_number: str) -> QWidget:
        """Создаёт виджет для одной карты"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Номер карты
        card_label = QLabel(self._format_card_number(card_number))
        card_label.setStyleSheet("""
            color: #d4d4d4;
            font-size: 13px;
            font-family: 'Consolas', 'Courier New', monospace;
            letter-spacing: 1px;
        """)
        layout.addWidget(card_label, 1)

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

        def paint_icon(event):
            painter = QPainter(copy_btn)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor(200, 200, 200), 1.5))
            painter.setBrush(Qt.NoBrush)

            painter.drawRect(QRect(6, 6, 14, 16))
            painter.drawLine(QRect(14, 6, 6, 6).topRight(), QRect(14, 6, 6, 6).bottomLeft())
            painter.drawLine(9, 12, 17, 12)
            painter.drawLine(9, 15, 17, 15)
            painter.drawLine(9, 18, 15, 18)
            painter.end()

        copy_btn.paintEvent = paint_icon
        copy_btn.clicked.connect(lambda checked, c=card_number: self.copy_card(c, copy_btn))
        layout.addWidget(copy_btn)

        widget.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-radius: 4px;
            }
            QWidget:hover { background-color: #2a2a2a; }
        """)

        return widget

    def copy_card(self, card_number: str, btn: QPushButton):
        """Копирует одну карту"""
        QApplication.clipboard().setText(card_number)

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
        """Копирует все карты"""
        if self.generated_cards:
            text = "\n".join(self.generated_cards)
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
            QPushButton:hover { background-color: #0078d4; color: white; }
        """)