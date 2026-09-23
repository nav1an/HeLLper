"""Сервис для управления напоминаниями"""
from PySide6.QtCore import QSettings, QDateTime, QTimer
from datetime import datetime
from typing import List, Dict, Optional


class ReminderService:
    """Сервис для управления напоминаниями"""

    def __init__(self, settings: QSettings):
        self.settings = settings
        self.reminders: List[Dict] = []
        self.active_timer: Optional[QTimer] = None
        self.on_reminder_triggered = None  # callback
        self.load_reminders()

    def load_reminders(self):
        """Загружает напоминания из настроек"""
        saved = self.settings.value("reminders", [])
        if isinstance(saved, list):
            self.reminders = saved
        else:
            self.reminders = []

    def save_reminders(self):
        """Сохраняет напоминания в настройки"""
        self.settings.setValue("reminders", self.reminders)

    def add_reminder(self, text: str, datetime_str: str) -> Dict:
        """Добавляет новое напоминание"""
        reminder = {
            "text": text,
            "datetime": datetime_str,
            "completed": False
        }
        self.reminders.append(reminder)
        self.reminders.sort(key=lambda x: x["datetime"])  # Сортировка по времени
        self.save_reminders()
        self.start_monitoring()
        return reminder

    def remove_reminder(self, index: int):
        """Удаляет напоминание по индексу"""
        if 0 <= index < len(self.reminders):
            self.reminders.pop(index)
            self.save_reminders()

    def get_reminders(self) -> List[Dict]:
        """Возвращает все напоминания"""
        return self.reminders

    def get_active_reminders(self) -> List[Dict]:
        """Возвращает только активные (не выполненные) напоминания"""
        return [r for r in self.reminders if not r["completed"]]

    def start_monitoring(self):
        """Запускает мониторинг напоминаний"""
        if self.active_timer:
            self.active_timer.stop()

        self.active_timer = QTimer()
        self.active_timer.timeout.connect(self.check_reminders)
        self.active_timer.start(1000)  # Проверяем каждую секунду

    def check_reminders(self):
        """Проверяет, не пришло ли время для напоминаний"""
        now = datetime.now()

        for i, reminder in enumerate(self.reminders):
            if reminder["completed"]:
                continue

            try:
                reminder_time = datetime.fromisoformat(reminder["datetime"])

                if now >= reminder_time:
                    # Время пришло!
                    reminder["completed"] = True
                    self.save_reminders()

                    if self.on_reminder_triggered:
                        self.on_reminder_triggered(reminder["text"], i)

                    break  # Обрабатываем по одному за раз
            except Exception:
                pass

    def reschedule_reminder(self, index: int, new_datetime_str: str):
        """Переносит напоминание на новое время"""
        if 0 <= index < len(self.reminders):
            self.reminders[index]["datetime"] = new_datetime_str
            self.reminders[index]["completed"] = False
            self.reminders.sort(key=lambda x: x["datetime"])
            self.save_reminders()
            self.start_monitoring()

    def clear_completed(self):
        """Удаляет все выполненные напоминания"""
        self.reminders = [r for r in self.reminders if not r["completed"]]
        self.save_reminders()