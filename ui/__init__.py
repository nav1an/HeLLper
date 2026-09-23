"""UI компоненты приложения"""
from .translator_panel import TranslatorPanel
from .settings_panel import SettingsPanel
from .clipboard_panel import ClipboardPanel
from .json_panel import JsonPanel
from .reminder_panel import ReminderPanel
from .uuid_panel import UuidPanel
from .char_counter_panel import CharCounterPanel
from .topbar_window import TopBarWindow

__all__ = [
    'TranslatorPanel',
    'SettingsPanel',
    'ClipboardPanel',
    'JsonPanel',
    'ReminderPanel',
    'UuidPanel',
    'CharCounterPanel',
    'TopBarWindow'
]