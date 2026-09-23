"""Точка входа в приложение HeLLper"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.topbar_window import TopBarWindow


def main():
    # Настройка для корректного отображения на экранах с высоким DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)

    # Создаем главное окно.
    # Оно само загрузит настройки и применит тему внутри своего __init__
    window = TopBarWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()