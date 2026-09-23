"""Менеджер тем оформления"""
from PySide6.QtGui import QColor
from PySide6.QtCore import QSettings
from typing import Dict
from config import APP_NAME, APP_ORG


class ThemeManager:
    """Управление темами приложения"""

    def __init__(self, settings: QSettings):
        self.settings = settings

    def get_theme(self) -> Dict:
        """Получить текущую тему"""
        theme_key = self.settings.value("theme", "dark_blue")

        themes = {
            "dark_blue": {
                "name": "Тёмная с синим",
                "bg_color": QColor("#1e1e1e"),
                "panel_bg": QColor("#252525"),
                "text_color": QColor("#ffffff"),
                "accent_color": QColor("#06297a"),
                "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:0.5 #06297a, stop:1 #1e1e1e)",
                "is_dark": True
            },
            "dark_red": {
                "name": "Тёмная с красным",
                "bg_color": QColor("#1e1e1e"),
                "panel_bg": QColor("#252525"),
                "text_color": QColor("#ffffff"),
                "accent_color": QColor("#7a0606"),
                "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:0.5 #7a0606, stop:1 #1e1e1e)",
                "is_dark": True
            },
            "dark_yellow": {
                "name": "Тёмная с жёлтым",
                "bg_color": QColor("#1e1e1e"),
                "panel_bg": QColor("#252525"),
                "text_color": QColor("#ffffff"),
                "accent_color": QColor("#f1c40f"),
                "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:0.5 #f1c40f, stop:1 #1e1e1e)",
                "is_dark": True
            },
            "dark_green": {
                "name": "Тёмная с зелёным",
                "bg_color": QColor("#1e1e1e"),
                "panel_bg": QColor("#252525"),
                "text_color": QColor("#ffffff"),
                "accent_color": QColor("#067a08"),
                "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:0.5 #067a08, stop:1 #1e1e1e)",
                "is_dark": True
            },
            "dark_turquoise": {
                "name": "Тёмная с бирюзовым",
                "bg_color": QColor("#1e1e1e"),
                "panel_bg": QColor("#252525"),
                "text_color": QColor("#ffffff"),
                "accent_color": QColor("#06baba"),
                "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:0.5 #06baba, stop:1 #1e1e1e)",
                "is_dark": True
            },
            "dark_pink": {
                "name": "Тёмная с розовым",
                "bg_color": QColor("#1e1e1e"),
                "panel_bg": QColor("#252525"),
                "text_color": QColor("#ffffff"),
                "accent_color": QColor("#ba0690"),
                "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1e1e, stop:0.5 #ba0690, stop:1 #1e1e1e)",
                "is_dark": True
            }
        }

        return themes.get(theme_key, themes["dark_blue"])

    def get_available_themes(self) -> Dict[str, str]:
        """Получить список доступных тем"""
        return {
            "dark_blue": "Тёмная с синим",
            "dark_red": "Тёмная с красным",
            "dark_yellow": "Тёмная с жёлтым",
            "dark_green": "Тёмная с зелёным",
            "dark_turquoise": "Тёмная с бирюзовым",
            "dark_pink": "Тёмная с розовым"
        }

    def set_theme(self, theme_key: str):
        """Установить тему"""
        self.settings.setValue("theme", theme_key)

    def get_current_theme_key(self) -> str:
        """Получить ключ текущей темы"""
        return self.settings.value("theme", "dark_blue")