"""Скрипт для создания .exe файла"""
import os
import PyInstaller.__main__

# Получаем абсолютный путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',
    '--onefile',              # Один файл
    '--windowed',             # Без консоли
    '--name', 'HeLLper',      # Имя программы
    '--icon', 'assets/icon.ico' if os.path.exists(os.path.join(current_dir, 'assets', 'icon.ico')) else '',
    '--add-data', 'config.py;.',  # Добавить config.py
    '--add-data', 'ui;ui',    # Добавить папку ui
    '--add-data', 'core;core', # Добавить папку core
    '--clean',                # Очистить перед сборкой
])

print("\n✅ Готово! .exe файл создан в папке 'dist'")