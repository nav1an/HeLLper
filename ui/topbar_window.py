"""Главное окно приложения"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, QTimer, QPoint, QSettings
from PySide6.QtGui import QCursor
from config import APP_NAME, APP_ORG, WINDOW_WIDTH, DROPDOWN_HEIGHT
from core.timezones import TimeZoneService
from core.theme_manager import ThemeManager
from .translator_panel import TranslatorPanel
from .settings_panel import SettingsPanel
from .clipboard_panel import ClipboardPanel
from .json_panel import JsonPanel
from .reminder_panel import ReminderPanel
from .reminder_popup import ReminderPopup
from .reschedule_dialog import RescheduleDialog
from .uuid_panel import UuidPanel
from .char_counter_panel import CharCounterPanel
from .card_generator_panel import CardGeneratorPanel
from core.translator import TranslatorService
from core.clipboard import ClipboardService
from core.reminder_service import ReminderService


class TopBarWindow(QWidget):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.menu_open = False

        self.is_pinned = True
        self.is_hidden = False
        self.base_y = 0
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._attempt_hide)

        self.settings = QSettings(APP_ORG, APP_NAME)
        self.timezone_service = TimeZoneService()
        self.translator_service = TranslatorService()
        self.clipboard_service = ClipboardService(self.settings)
        self.theme_manager = ThemeManager(self.settings)
        self.reminder_service = ReminderService(self.settings)

        self.current_timezone = self.settings.value("timezone", None)

        self.init_ui()
        self.init_timers()

        theme = self.theme_manager.get_theme()
        self.apply_theme(theme)

    def is_tool_enabled(self, tool_key: str) -> bool:
        return self.settings.value(f"tool_{tool_key}", True, type=bool)

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Верхняя плашка ---
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(40)

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(15, 0, 15, 0)
        top_layout.setSpacing(10)

        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("""
            color: white; 
            font-size: 16px; 
            font-weight: bold;
            background: transparent;
        """)

        self.app_title = QLabel("👹HeLLper")
        self.app_title.setStyleSheet("""
            color: #ff4444;
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 1px;
            background: transparent;
        """)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                color: white; 
                border: none;
                font-size: 16px; 
                border-radius: 15px; 
            }
            QPushButton:hover { 
                background-color: #e74c3c; 
                color: white;
            }
        """)
        self.close_btn.clicked.connect(self.close)

        self.arrow_btn = QPushButton("▼")
        self.arrow_btn.setFixedSize(30, 30)
        self.arrow_btn.setCursor(Qt.PointingHandCursor)
        self.arrow_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                color: white; 
                border: none;
                font-size: 14px; 
                border-radius: 15px; 
            }
            QPushButton:hover { 
                background-color: #3e3e3e; 
            }
        """)
        self.arrow_btn.clicked.connect(self.toggle_menu)

        self.pin_btn = QPushButton("🖈")
        self.pin_btn.setFixedSize(30, 30)
        self.pin_btn.setCursor(Qt.PointingHandCursor)
        self.pin_btn.setToolTip("Закрепить панель")
        self.pin_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                color: white; 
                border: none;
                font-size: 14px; 
                border-radius: 15px; 
            }
            QPushButton:hover { 
                background-color: #3e3e3e; 
            }
        """)
        self.pin_btn.clicked.connect(self.toggle_pin)

        top_layout.addWidget(self.time_label)
        top_layout.addStretch()
        top_layout.addWidget(self.app_title)
        top_layout.addStretch()
        top_layout.addWidget(self.pin_btn)
        top_layout.addWidget(self.arrow_btn)
        top_layout.addWidget(self.close_btn)

        # --- Выпадающее меню ---
        self.dropdown = QWidget()
        self.dropdown.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.dropdown.setAttribute(Qt.WA_TranslucentBackground, False)
        self.dropdown.setFixedHeight(DROPDOWN_HEIGHT)
        self.dropdown.setFixedWidth(WINDOW_WIDTH)
        self.dropdown.setStyleSheet("background-color: #1e1e1e; border: 1px solid #3e3e3e;")
        self.dropdown.hide()

        drop_layout = QHBoxLayout(self.dropdown)
        drop_layout.setContentsMargins(0, 0, 0, 0)

        # Боковая панель (СОХРАНЯЕМ КАК АТРИБУТ!)
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(60)
        self.sidebar.setStyleSheet("background-color: #252525; border-right: 1px solid #3e3e3e;")
        self.side_layout = QVBoxLayout(self.sidebar)
        self.side_layout.setContentsMargins(0, 20, 0, 10)
        self.side_layout.setSpacing(15)

        # Создаём кнопки инструментов
        self._side_buttons = []
        self._build_sidebar_buttons()

        # Область контента
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: #1e1e1e; color: white;")

        # Создаём панели
        self._build_content_panels()

        drop_layout.addWidget(self.sidebar)
        drop_layout.addWidget(self.content_area, 1)

        main_layout.addWidget(self.top_bar)

        self.setFixedWidth(WINDOW_WIDTH)
        self.adjustSize()
        self.center_on_screen()

        self.base_y = self.y()

        self.apply_timezone(self.current_timezone)
        self.switch_panel(0)

    def _build_sidebar_buttons(self):
        """Создаёт кнопки в sidebar"""
        # Очищаем старые кнопки (кроме stretch)
        while self.side_layout.count() > 0:
            item = self.side_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._side_buttons = []
        panel_index = 0

        tools_order = [
            ("json", "{ }"),
            ("uuid", "🆔"),
            ("translator", "🔠"),
            ("reminder", "💬"),
            ("clipboard", "💾"),
            ("counter", "Aa"),
            ("card", "💳"),
        ]

        for tool_key, icon in tools_order:
            if self.is_tool_enabled(tool_key):
                btn = self._make_side_button(icon)
                btn.clicked.connect(lambda checked, idx=panel_index: self.switch_panel(idx))
                self.side_layout.addWidget(btn, alignment=Qt.AlignCenter)
                self._side_buttons.append(btn)
                panel_index += 1

        # Stretch
        self.side_layout.addStretch()

        # Кнопка настроек (всегда)
        self.settings_btn = self._make_side_button("⚙")
        settings_index = panel_index
        self.settings_btn.clicked.connect(lambda checked, idx=settings_index: self.switch_panel(idx))
        self.side_layout.addWidget(self.settings_btn, alignment=Qt.AlignCenter)
        self._side_buttons.append(self.settings_btn)

    def _build_content_panels(self):
        """Создаёт панели контента"""
        # Очищаем старые панели
        while self.content_area.count() > 0:
            widget = self.content_area.widget(0)
            self.content_area.removeWidget(widget)
            widget.deleteLater()

        if self.is_tool_enabled("json"):
            self.json_panel = JsonPanel()
            self.content_area.addWidget(self.json_panel)

        if self.is_tool_enabled("uuid"):
            self.uuid_panel = UuidPanel()
            self.content_area.addWidget(self.uuid_panel)

        if self.is_tool_enabled("translator"):
            self.translator_panel = TranslatorPanel(self.translator_service)
            self.content_area.addWidget(self.translator_panel)

        if self.is_tool_enabled("reminder"):
            self.reminder_panel = ReminderPanel(self.reminder_service)
            self.reminder_service.on_reminder_triggered = self.on_reminder_triggered
            self.content_area.addWidget(self.reminder_panel)

        if self.is_tool_enabled("clipboard"):
            self.clipboard_panel = ClipboardPanel(self.clipboard_service)
            self.content_area.addWidget(self.clipboard_panel)

        if self.is_tool_enabled("counter"):
            self.counter_panel = CharCounterPanel()
            self.content_area.addWidget(self.counter_panel)

        if self.is_tool_enabled("card"):
            self.card_panel = CardGeneratorPanel()
            self.content_area.addWidget(self.card_panel)

        # Настройки (всегда)
        self.settings_panel = SettingsPanel(self.settings)
        self.settings_panel.timezone_changed = self.on_timezone_changed
        self.settings_panel.theme_changed = self.on_theme_changed
        self.settings_panel.tools_changed = self.refresh_sidebar
        self.content_area.addWidget(self.settings_panel)

    def _make_side_button(self, icon):
        btn = QPushButton(icon)
        btn.setFixedSize(40, 40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                color: white; 
                border: none;
                font-size: 18px; 
                border-radius: 4px;
            }
            QPushButton:hover { 
                background-color: #3e3e3e; 
            }
        """)
        return btn

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        self.move(x, 0)
        self.base_y = 0

    def init_timers(self):
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        try:
            now, _ = self.timezone_service.get_datetime(self.current_timezone)
            self.time_label.setText(now.strftime("%H:%M"))
        except Exception:
            self.time_label.setText("--:--")

    def apply_timezone(self, tz_key):
        self.current_timezone = tz_key
        self.settings.setValue("timezone", tz_key)
        self.update_time()

    def on_timezone_changed(self, tz_key):
        self.apply_timezone(tz_key)

    def apply_theme(self, theme):
        accent = theme["accent_color"]
        text_color = theme["text_color"]
        bg_color = theme["bg_color"]
        panel_bg = theme["panel_bg"]
        is_dark = theme["is_dark"]
        gradient = theme.get("gradient")

        title_color = "#ffffff" if is_dark else accent.name()
        self.app_title.setStyleSheet(f"""
            color: {title_color};
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 1px;
            background: transparent;
        """)

        if gradient:
            self.top_bar.setStyleSheet(f"background: {gradient};")
        else:
            self.top_bar.setStyleSheet(f"background-color: {bg_color.name()};")

        self.dropdown.setStyleSheet(
            f"background-color: {panel_bg.name()}; border: 1px solid #3e3e3e;"
        )
        self.content_area.setStyleSheet(
            f"background-color: {panel_bg.name()}; color: {text_color.name()};"
        )

        self.time_label.setStyleSheet(f"color: {text_color.name()}; font-size: 16px; font-weight: bold; background: transparent;")

        icon_color = accent.name()
        self.arrow_btn.setStyleSheet(f"""
            QPushButton {{ 
                background: transparent; 
                color: {icon_color}; 
                border: none;
                font-size: 14px; 
                border-radius: 15px; 
            }}
            QPushButton:hover {{ 
                background-color: #3e3e3e; 
            }}
        """)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{ 
                background: transparent; 
                color: {icon_color}; 
                border: none;
                font-size: 16px; 
                border-radius: 15px; 
            }}
            QPushButton:hover {{ 
                background-color: #e74c3c; 
                color: white;
            }}
        """)

        active_style = f"""
            QPushButton {{ background: {accent.name()}; color: white; border: none;
                         font-size: 18px; border-radius: 4px; }}
        """
        inactive_style = f"""
            QPushButton {{ background: transparent; color: {text_color.name()}; border: none;
                         font-size: 18px; border-radius: 4px; }}
            QPushButton:hover {{ background-color: #3e3e3e; }}
        """

        self._active_style = active_style
        self._inactive_style = inactive_style

        current_index = self.content_area.currentIndex()
        self.switch_panel(current_index)

    def on_theme_changed(self, theme):
        self.apply_theme(theme)

    def on_reminder_triggered(self, text: str, index: int):
        popup = ReminderPopup(text, self)

        def on_reschedule():
            popup.close()
            dialog = RescheduleDialog(self)
            if dialog.exec():
                new_datetime = dialog.get_selected_datetime()
                if new_datetime:
                    datetime_str = new_datetime.toString("yyyy-MM-ddTHH:mm:ss")
                    self.reminder_service.reschedule_reminder(index, datetime_str)
                    self.reminder_panel.refresh_list()

        popup.on_reschedule = on_reschedule
        popup.exec()

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.settings.setValue("pinned", self.is_pinned)

        if self.is_pinned:
            self.hide_timer.stop()
            self.move(self.x(), self.base_y)
            self.is_hidden = False
            self.pin_btn.setStyleSheet("""
                QPushButton { 
                    background: rgba(255, 255, 255, 0.2); 
                    color: white; 
                    border: none;
                    font-size: 14px; 
                    border-radius: 15px; 
                }
            """)
        else:
            self.pin_btn.setStyleSheet("""
                QPushButton { 
                    background: transparent; 
                    color: rgba(255, 255, 255, 0.5); 
                    border: none;
                    font-size: 14px; 
                    border-radius: 15px; 
                }
            """)

    def toggle_menu(self):
        if self.is_hidden:
            self.move(self.x(), self.base_y)
            self.is_hidden = False
            self.hide_timer.stop()

        screen = QApplication.primaryScreen().geometry()
        window_pos = self.pos()
        window_y = window_pos.y()
        window_bottom = window_y + self.height()
        space_below = screen.height() - window_bottom

        if self.menu_open:
            self.dropdown.hide()
            self.menu_open = False
            self.arrow_btn.setText("▼")
        else:
            self.dropdown.show()
            self.dropdown.activateWindow()
            self.dropdown.raise_()
            self.menu_open = True

            if space_below >= DROPDOWN_HEIGHT:
                dropdown_pos = QPoint(window_pos.x(), window_y + self.top_bar.height())
                self.dropdown.move(dropdown_pos)
                self.arrow_btn.setText("▲")
            else:
                dropdown_pos = QPoint(window_pos.x(), window_y - DROPDOWN_HEIGHT)
                self.dropdown.move(dropdown_pos)
                self.arrow_btn.setText("▼")

    def switch_panel(self, index):
        self.content_area.setCurrentIndex(index)

        if hasattr(self, '_active_style') and hasattr(self, '_inactive_style'):
            active_style = self._active_style
            inactive_style = self._inactive_style
        else:
            active_style = """
                QPushButton { background: #0078d4; color: white; border: none;
                             font-size: 18px; border-radius: 4px; }
            """
            inactive_style = """
                QPushButton { background: transparent; color: white; border: none;
                             font-size: 18px; border-radius: 4px; }
                QPushButton:hover { background-color: #3e3e3e; }
            """

        for btn in self._side_buttons:
            btn.setStyleSheet(inactive_style)

        if 0 <= index < len(self._side_buttons):
            self._side_buttons[index].setStyleSheet(active_style)

    def refresh_sidebar(self):
        """Обновляет sidebar и панели БЕЗ пересоздания окна"""
        # Запоминаем, что мы в настройках
        menu_was_open = self.menu_open

        if menu_was_open:
            self.dropdown.hide()
            self.menu_open = False

        # Пересоздаём кнопки в sidebar
        self._build_sidebar_buttons()

        # Пересоздаём панели контента
        self._build_content_panels()

        # Открываем настройки (последний индекс)
        settings_index = len(self._side_buttons) - 1
        self.switch_panel(settings_index)

        # Применяем тему к новым виджетам
        theme = self.theme_manager.get_theme()
        self.apply_theme(theme)

        # Восстанавливаем меню
        if menu_was_open:
            QTimer.singleShot(100, self.toggle_menu)

    def closeEvent(self, event):
        if self.menu_open:
            self.dropdown.close()
            self.menu_open = False
        event.accept()

    def enterEvent(self, event):
        self.hide_timer.stop()
        if self.is_hidden and not self.is_pinned:
            self.move(self.x(), self.base_y)
            self.is_hidden = False
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_pinned:
            self.hide_timer.start(600)
        super().leaveEvent(event)

    def _attempt_hide(self):
        if self.is_pinned or self.menu_open:
            return

        cursor_pos = QCursor.pos()
        over_main = self.geometry().contains(cursor_pos)
        over_dropdown = self.dropdown.geometry().contains(cursor_pos) if self.menu_open else False

        if not over_main and not over_dropdown:
            self.move(self.x(), self.base_y - 36)
            self.is_hidden = True