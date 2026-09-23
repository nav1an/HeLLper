"""Панель настроек"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt, QSettings
from core.timezones import TimeZoneService
from core.theme_manager import ThemeManager


class SettingsPanel(QWidget):
    """Панель настроек приложения"""

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        self.timezone_service = TimeZoneService()
        self.theme_manager = ThemeManager(settings)
        self.timezone_changed = None
        self.theme_changed = None
        self.tools_changed = None

        # Доступные инструменты
        self.available_tools = [
            {"key": "json", "name": "Форматирование JSON", "icon": "{ }"},
            {"key": "uuid", "name": "Генератор UUID", "icon": "🆔"},
            {"key": "translator", "name": "Переводчик", "icon": ""},
            {"key": "reminder", "name": "Напоминания", "icon": ""},
            {"key": "clipboard", "name": "Буфер обмена", "icon": "💾"},
            {"key": "counter", "name": "Счётчик символов", "icon": "Aa"},
            {"key": "card", "name": "Генератор карт", "icon": "💳"},
        ]

        self.init_ui()

    def init_ui(self):
        # ГЛАВНЫЙ layout с прокруткой
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ScrollArea для всей панели
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #3e3e3e;
                width: 6px;
                margin: 0;
                border-radius: 3px;
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

        # Контейнер для всех секций
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(15, 10, 15, 10)
        container_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Настройки")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        container_layout.addWidget(title)

        # ========== ЧАСОВОЙ ПОЯС ==========
        tz_section = QWidget()
        tz_section.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
            }
        """)
        tz_layout = QVBoxLayout(tz_section)
        tz_layout.setContentsMargins(10, 10, 10, 10)
        tz_layout.setSpacing(8)

        tz_title = QLabel("Часовой пояс")
        tz_title.setStyleSheet("color: #888; font-size: 11px; font-weight: bold;")
        tz_layout.addWidget(tz_title)

        self.tz_combo = QComboBox()
        self.tz_combo.setCursor(Qt.PointingHandCursor)
        self.tz_combo.setFixedHeight(32)
        self.tz_combo.setStyleSheet("""
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

        timezones = self.timezone_service.get_all_timezones()
        for tz in timezones:
            self.tz_combo.addItem(tz["name"], tz["key"])

        current_tz = self.settings.value("timezone", None)
        if current_tz:
            index = self.tz_combo.findData(current_tz)
            if index >= 0:
                self.tz_combo.setCurrentIndex(index)

        self.tz_combo.currentIndexChanged.connect(self.on_timezone_change)
        tz_layout.addWidget(self.tz_combo)
        container_layout.addWidget(tz_section)

        # ========== АВТОЗАПУСК ==========
        startup_section = QWidget()
        startup_section.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
            }
        """)
        startup_layout = QHBoxLayout(startup_section)
        startup_layout.setContentsMargins(10, 10, 10, 10)
        startup_layout.setSpacing(8)

        startup_title = QLabel("Автозапуск")
        startup_title.setStyleSheet("color: #888; font-size: 11px; font-weight: bold;")
        startup_layout.addWidget(startup_title)

        startup_label = QLabel("Запускать при старте Windows")
        startup_label.setStyleSheet("color: white; font-size: 12px;")
        startup_layout.addWidget(startup_label)
        startup_layout.addStretch()

        self.startup_toggle = QPushButton()
        self.startup_toggle.setFixedSize(50, 26)
        self.startup_toggle.setCursor(Qt.PointingHandCursor)
        self.startup_toggle.clicked.connect(self.toggle_startup)
        startup_layout.addWidget(self.startup_toggle)

        self._update_startup_toggle()
        container_layout.addWidget(startup_section)

        # ========== ИНСТРУМЕНТЫ ==========
        tools_section = QWidget()
        tools_section.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
            }
        """)
        tools_layout = QVBoxLayout(tools_section)
        tools_layout.setContentsMargins(10, 10, 10, 10)
        tools_layout.setSpacing(8)

        tools_title = QLabel("Инструменты")
        tools_title.setStyleSheet("color: #888; font-size: 11px; font-weight: bold;")
        tools_layout.addWidget(tools_title)

        for tool in self.available_tools:
            tool_widget = self._create_tool_row(tool)
            tools_layout.addWidget(tool_widget)

        container_layout.addWidget(tools_section)

        # ========== ТЕМА ==========
        theme_section = QWidget()
        theme_section.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
            }
        """)
        theme_layout = QVBoxLayout(theme_section)
        theme_layout.setContentsMargins(10, 10, 10, 10)
        theme_layout.setSpacing(8)

        theme_title = QLabel("Тема")
        theme_title.setStyleSheet("color: #888; font-size: 11px; font-weight: bold;")
        theme_layout.addWidget(theme_title)

        self.theme_combo = QComboBox()
        self.theme_combo.setCursor(Qt.PointingHandCursor)
        self.theme_combo.setFixedHeight(32)
        self.theme_combo.addItems([
            "Тёмная с синим",
            "Тёмная с красным",
            "Тёмная с жёлтым",
            "Тёмная с зелёным",
            "Тёмная с бирюзовым",
            "Тёмная с розовым",
        ])
        self.theme_combo.setStyleSheet("""
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

        current_theme = self.theme_manager.get_current_theme_key()
        theme_keys = ["dark_blue", "dark_red", "dark_yellow", "dark_green", "dark_turquoise", "dark_pink", "light_blue", "light_red"]
        if current_theme in theme_keys:
            self.theme_combo.setCurrentIndex(theme_keys.index(current_theme))

        self.theme_combo.currentIndexChanged.connect(self.on_theme_change)
        theme_layout.addWidget(self.theme_combo)
        container_layout.addWidget(theme_section)

        container_layout.addStretch()

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    def _create_tool_row(self, tool: dict) -> QWidget:
        """Создаёт строку для инструмента"""
        widget = QWidget()
        widget.setFixedHeight(36)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(10)

        # Иконка + название
        tool_label = QLabel(f"{tool['icon']}  {tool['name']}")
        tool_label.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(tool_label)

        layout.addStretch()

        # Кнопка-переключатель
        toggle_btn = QPushButton()
        toggle_btn.setFixedSize(50, 26)
        toggle_btn.setCursor(Qt.PointingHandCursor)
        toggle_btn.clicked.connect(lambda checked, k=tool["key"], b=toggle_btn: self.toggle_tool(k, b))
        layout.addWidget(toggle_btn)

        # Загружаем состояние
        is_enabled = self.settings.value(f"tool_{tool['key']}", True, type=bool)
        self._update_tool_toggle(toggle_btn, is_enabled)

        return widget

    def _update_tool_toggle(self, btn: QPushButton, is_enabled: bool):
        """Обновляет вид переключателя инструмента"""
        if is_enabled:
            btn.setText("ВКЛ")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 10px;
                    font-size: 11px;
                    font-weight: bold;
                }
            """)
        else:
            btn.setText("ВЫКЛ")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #555;
                    color: #888;
                    border: none;
                    border-radius: 4px;
                    padding: 0 10px;
                    font-size: 11px;
                }
            """)

    def toggle_tool(self, tool_key: str, btn: QPushButton):
        """Переключает инструмент"""
        is_enabled = self.settings.value(f"tool_{tool_key}", True, type=bool)
        self.settings.setValue(f"tool_{tool_key}", not is_enabled)
        self._update_tool_toggle(btn, not is_enabled)

        if self.tools_changed:
            self.tools_changed()

    def _update_startup_toggle(self):
        """Обновляет вид переключателя автозапуска"""
        is_enabled = self.settings.value("autostart", False, type=bool)

        if is_enabled:
            self.startup_toggle.setText("ВКЛ")
            self.startup_toggle.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 10px;
                    font-size: 11px;
                    font-weight: bold;
                }
            """)
        else:
            self.startup_toggle.setText("ВЫКЛ")
            self.startup_toggle.setStyleSheet("""
                QPushButton {
                    background-color: #555;
                    color: #888;
                    border: none;
                    border-radius: 4px;
                    padding: 0 10px;
                    font-size: 11px;
                }
            """)

    def toggle_startup(self):
        """Переключает автозапуск"""
        is_enabled = self.settings.value("autostart", False, type=bool)
        self.settings.setValue("autostart", not is_enabled)
        self._update_startup_toggle()

    def on_timezone_change(self, index):
        """При смене часового пояса"""
        tz_key = self.tz_combo.itemData(index)
        if tz_key and self.timezone_changed:
            self.timezone_changed(tz_key)

    def on_theme_change(self, index):
        """При смене темы"""
        theme_keys = ["dark_blue", "dark_red", "dark_yellow", "dark_green", "dark_turquoise", "dark_pink", "light_blue", "light_red"]
        if 0 <= index < len(theme_keys):
            theme_key = theme_keys[index]
            self.theme_manager.set_theme(theme_key)
            if self.theme_changed:
                theme = self.theme_manager.get_theme()
                self.theme_changed(theme)