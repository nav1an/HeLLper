@echo off
echo ============================================
echo Сборка HeLLper в .exe через Nuitka
echo ============================================
echo.

echo [1/3] Очистка старой сборки...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "hellper.build" rmdir /s /q "hellper.build"

echo [2/3] Сборка...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=icon.ico ^
    --enable-plugin=pyside6 ^
    --include-package=PySide6 ^
    --include-package=core ^
    --include-package=ui ^
    --output-dir=dist ^
    --output-filename=HeLLper.exe ^
    main.py

echo.
echo [3/3] Готово!
echo Файл находится в папке: dist\HeLLper.exe
echo ============================================
pause