"""Сервис для работы с буфером обмена"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings
from typing import List, Dict


class ClipboardService:
    """Сервис для мониторинга и хранения истории буфера обмена"""

    def __init__(self, settings: QSettings, max_items: int = 30):
        self.settings = settings
        self.max_items = max_items
        self.clipboard = QApplication.clipboard()
        self.history: List[Dict] = []
        self.load_history()

    def load_history(self):
        saved = self.settings.value("clipboard_history", [])
        if isinstance(saved, list):
            # Фильтруем битые записи
            self.history = [
                item for item in saved
                if isinstance(item, dict) and item.get("text", "").strip()
            ]
        else:
            self.history = []

    def save_history(self):
        self.settings.setValue("clipboard_history", self.history)

    def add_to_history(self, text: str):
        """Добавляет текст в историю"""
        # Фильтруем пустые и пробельные тексты
        if not text or not text.strip():
            return

        # Не добавляем дубликаты
        if any(item.get("text") == text for item in self.history):
            return

        # Добавляем в начало
        self.history.insert(0, {"text": text, "pinned": False})

        # Обрезаем до лимита
        self._trim_history()
        self.save_history()

    def _trim_history(self):
        """Удаляет лишние не закреплённые элементы, сохраняя закреплённые"""
        pinned = [item for item in self.history if item.get("pinned")]
        unpinned = [item for item in self.history if not item.get("pinned")]

        # Максимум не закреплённых = max_items - количество закреплённых
        max_unpinned = max(0, self.max_items - len(pinned))
        unpinned = unpinned[:max_unpinned]

        self.history = pinned + unpinned

    def toggle_pin(self, index: int):
        """Закрепить/открепить элемент"""
        if 0 <= index < len(self.history):
            self.history[index]["pinned"] = not self.history[index]["pinned"]
            self._reorder_history()
            self.save_history()

    def _reorder_history(self):
        """Перемещает закреплённые элементы вверх"""
        pinned = [item for item in self.history if item.get("pinned")]
        unpinned = [item for item in self.history if not item.get("pinned")]
        self.history = pinned + unpinned

    def get_history(self) -> List[Dict]:
        return self.history

    def clear_history(self):
        """Очищает только не закреплённые"""
        self.history = [item for item in self.history if item.get("pinned")]
        self.save_history()

    def clear_all_history(self):
        """Полностью очищает историю"""
        self.history = []
        self.save_history()

    def get_clipboard_text(self) -> str:
        return self.clipboard.text()

    def set_clipboard_text(self, text: str):
        self.clipboard.setText(text)