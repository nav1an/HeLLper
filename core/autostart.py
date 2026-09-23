"""Сервис автозапуска с Windows"""
import sys
import os
from pathlib import Path
import winreg


class AutoStartService:
    """Сервис для управления автозапуском"""

    REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def __init__(self, app_name: str = "HeLLper"):
        self.app_name = app_name

    def _get_app_path(self) -> str:
        """Получает путь к запуску программы"""
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            script_dir = Path(__file__).parent.parent
            bat_path = script_dir / "run.bat"

            if bat_path.exists():
                return str(bat_path)
            else:
                # Используем pythonw.exe вместо python.exe
                pythonw_path = Path(sys.executable).parent / "pythonw.exe"
                if pythonw_path.exists():
                    main_path = script_dir / "main.py"
                    return f'"{pythonw_path}" "{main_path}"'
                else:
                    main_path = script_dir / "main.py"
                    return f'"{sys.executable}" "{main_path}"'

    def is_enabled(self) -> bool:
        """Проверяет, включен ли автозапуск"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.REGISTRY_KEY,
                0,
                winreg.KEY_READ
            )
            value, _ = winreg.QueryValueEx(key, self.app_name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def enable(self) -> bool:
        """Включает автозапуск"""
        try:
            app_path = self._get_app_path()

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Ошибка включения автозапуска: {e}")
            return False

    def disable(self) -> bool:
        """Отключает автозапуск"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, self.app_name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return True  # Уже отключен
        except Exception as e:
            print(f"Ошибка отключения автозапуска: {e}")
            return False