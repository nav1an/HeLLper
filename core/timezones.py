"""Сервис для работы с часовыми поясами"""
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


class TimeZoneService:
    """Сервис для получения времени по разным часовым поясам"""

    def __init__(self):
        self.timezones = [
            {"key": "Europe/Kaliningrad", "name": "Калининград (UTC+2)"},
            {"key": "Europe/Moscow", "name": "Москва (UTC+3)"},
            {"key": "Europe/Samara", "name": "Самара (UTC+4)"},
            {"key": "Asia/Yekaterinburg", "name": "Екатеринбург (UTC+5)"},
            {"key": "Asia/Omsk", "name": "Омск (UTC+6)"},
            {"key": "Asia/Krasnoyarsk", "name": "Красноярск (UTC+7)"},
            {"key": "Asia/Irkutsk", "name": "Иркутск (UTC+8)"},
            {"key": "Asia/Yakutsk", "name": "Якутск (UTC+9)"},
            {"key": "Asia/Vladivostok", "name": "Владивосток (UTC+10)"},
            {"key": "Asia/Magadan", "name": "Магадан (UTC+11)"},
            {"key": "Asia/Kamchatka", "name": "Камчатка (UTC+12)"},
        ]

    def get_all_timezones(self):
        """Возвращает список всех доступных часовых поясов"""
        return self.timezones

    def get_datetime(self, tz_key):
        """Возвращает текущее время и строку смещения для указанного пояса"""
        try:
            tz = ZoneInfo(tz_key)
            now = datetime.now(tz)
            offset = now.strftime("%z")
            offset_str = f"UTC{offset[:3]}:{offset[3:]}"
            return now, offset_str
        except Exception:
            # Фоллбэк на Москву
            tz = ZoneInfo("Europe/Moscow")
            now = datetime.now(tz)
            return now, "UTC+3"

    def get_offset_string(self, tz_key):
        """Возвращает строку смещения для пояса"""
        try:
            tz = ZoneInfo(tz_key)
            now = datetime.now(tz)
            offset = now.strftime("%z")
            return f"UTC{offset[:3]}:{offset[3:]}"
        except Exception:
            return "UTC+3"