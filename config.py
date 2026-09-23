"""Конфигурация приложения"""

# API настройки
TRANSLATOR_API_URL = "https://api.mymemory.translated.net/get"

# Доступные языки для переводчика
AVAILABLE_LANGUAGES = {
    "English": "en",
    "Русский": "ru",
    "Deutsch": "de",
    "Français": "fr",
    "Español": "es",
    "Italiano": "it",
    "中文": "zh",
    "日本語": "ja"
}

# Российские часовые пояса (fallback)
RUSSIAN_TIMEZONES = {
    "Europe/Kaliningrad": 2,
    "Europe/Moscow": 3,
    "Europe/Simferopol": 3,
    "Europe/Kirov": 3,
    "Europe/Volgograd": 3,
    "Europe/Saratov": 3,
    "Europe/Astrakhan": 3,
    "Europe/Ulyanovsk": 3,
    "Europe/Samara": 4,
    "Europe/Izhevsk": 4,
    "Asia/Yekaterinburg": 5,
    "Asia/Chelyabinsk": 5,
    "Asia/Tyumen": 5,
    "Asia/Kurgan": 5,
    "Asia/Omsk": 6,
    "Asia/Krasnoyarsk": 7,
    "Asia/Novokuznetsk": 7,
    "Asia/Novosibirsk": 7,
    "Asia/Tomsk": 7,
    "Asia/Barnaul": 7,
    "Asia/Irkutsk": 8,
    "Asia/Chita": 8,
    "Asia/Yakutsk": 9,
    "Asia/Khandyga": 9,
    "Asia/Vladivostok": 10,
    "Asia/Ust-Nera": 10,
    "Asia/Sakhalin": 10,
    "Asia/Magadan": 11,
    "Asia/Srednekolymsk": 11,
    "Asia/Kamchatka": 12,
    "Asia/Anadyr": 12,
}

# Популярные пояса для UI
POPULAR_TIMEZONES = [
    ("Системное время", None),
    ("Калининград (UTC+2)", "Europe/Kaliningrad"),
    ("Москва (UTC+3)", "Europe/Moscow"),
    ("Самара (UTC+4)", "Europe/Samara"),
    ("Екатеринбург (UTC+5)", "Asia/Yekaterinburg"),
    ("Омск (UTC+6)", "Asia/Omsk"),
    ("Красноярск (UTC+7)", "Asia/Krasnoyarsk"),
    ("Иркутск (UTC+8)", "Asia/Irkutsk"),
    ("Якутск (UTC+9)", "Asia/Yakutsk"),
    ("Владивосток (UTC+10)", "Asia/Vladivostok"),
    ("Магадан (UTC+11)", "Asia/Magadan"),
    ("Камчатка (UTC+12)", "Asia/Kamchatka"),
]

# Настройки приложения
APP_NAME = "TopBarApp"
APP_ORG = "TopBarApp"
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 40
DROPDOWN_HEIGHT = 400