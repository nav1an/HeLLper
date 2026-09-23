"""Сервис для форматирования JSON"""
import json
from typing import Tuple


class JsonFormatterService:
    """Сервис для форматирования и валидации JSON"""

    def format_json(self, raw_text: str, indent: int = 4) -> Tuple[str, bool]:
        """
        Форматирует JSON текст

        Args:
            raw_text: сырой JSON текст
            indent: количество пробелов для отступа

        Returns:
            Tuple[formatted_text, is_valid]
        """
        try:
            # Пытаемся распарсить JSON
            parsed = json.loads(raw_text)

            # Форматируем с отступами
            formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)

            return formatted, True
        except json.JSONDecodeError as e:
            return f"Ошибка: {str(e)}", False
        except Exception as e:
            return f"Неизвестная ошибка: {str(e)}", False

    def minify_json(self, raw_text: str) -> Tuple[str, bool]:
        """Сжимает JSON в одну строку"""
        try:
            parsed = json.loads(raw_text)
            formatted = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
            return formatted, True
        except json.JSONDecodeError as e:
            return f"Ошибка: {str(e)}", False
        except Exception as e:
            return f"Неизвестная ошибка: {str(e)}", False