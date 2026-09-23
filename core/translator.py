"""Сервис перевода"""
import httpx
from typing import Optional
from config import TRANSLATOR_API_URL, AVAILABLE_LANGUAGES


class TranslatorService:
    """Сервис для работы с переводчиком MyMemory"""

    def __init__(self):
        self.api_url = TRANSLATOR_API_URL
        self.lang_map = AVAILABLE_LANGUAGES

    def translate(self, text: str, source: str, target: str) -> tuple[str, Optional[str]]:
        """
        Переводит текст.

        Args:
            text: Текст для перевода
            source: Исходный язык (например, "English")
            target: Целевой язык (например, "Русский")

        Returns:
            Кортеж (переведённый_текст, ошибка)
        """
        if not text.strip():
            return "", None

        src_code = self.lang_map.get(source, "en")
        dst_code = self.lang_map.get(target, "ru")
        langpair = f"{src_code}|{dst_code}"

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    self.api_url,
                    params={"q": text, "langpair": langpair}
                )
                data = response.json()

                if data.get("responseStatus") == 200:
                    return data["responseData"]["translatedText"], None
                else:
                    return "", data.get("responseDetails", "Неизвестная ошибка")
        except httpx.TimeoutException:
            return "", "Превышено время ожидания"
        except Exception as e:
            return "", f"Ошибка сети: {str(e)}"

    def get_available_languages(self) -> list[str]:
        """Возвращает список доступных языков"""
        return list(self.lang_map.keys())