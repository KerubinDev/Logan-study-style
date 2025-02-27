import os
from pathlib import Path

# Configurações básicas do aplicativo
APP_NAME = "AnimeProductivity Suite"
APP_VERSION = "1.0.0"

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configurações do banco de dados
DATABASE = {
    'default': {
        'ENGINE': 'sqlite',
        'NAME': os.path.join(BASE_DIR, 'data', 'animeproductivity.db'),
    }
}

# Configurações do Pomodoro
POMODORO_DEFAULTS = {
    'work_time': 25,  # minutos
    'break_time': 5,  # minutos
    'long_break_time': 15,  # minutos
    'long_break_interval': 4  # número de pomodoros antes do intervalo longo
}

# Configurações de tema
THEMES = {
    'dark': {
        'primary': '#1a1b26',
        'secondary': '#24283b',
        'accent': '#7aa2f7',
        'text': '#a9b1d6',
        'error': '#f7768e'
    },
    'light': {
        'primary': '#d5d6db',
        'secondary': '#9699a3',
        'accent': '#2ac3de',
        'text': '#343b58',
        'error': '#f7768e'
    }
}

# Configurações de autenticação
AUTH = {
    'TOKEN_EXPIRY': 24 * 60 * 60,  # 24 horas em segundos
    'MIN_PASSWORD_LENGTH': 8,
    'REQUIRE_SPECIAL_CHARS': True
}

# Configurações da API do Google Calendar
GOOGLE_CALENDAR = {
    'credentials_file': os.path.join(BASE_DIR, 'config', 'credentials.json'),
    'token_file': os.path.join(BASE_DIR, 'config', 'token.json'),
    'scopes': ['https://www.googleapis.com/auth/calendar.readonly',
               'https://www.googleapis.com/auth/calendar.events']
}

# Adicionar às configurações existentes

GOOGLE_API = {
    'credentials_file': 'credentials.json',
    'token_directory': 'tokens'
}

DISTRACTION_DEFAULTS = {
    "Redes Sociais": [
        "facebook.com",
        "twitter.com",
        "instagram.com",
        "tiktok.com"
    ],
    "Entretenimento": [
        "youtube.com",
        "netflix.com",
        "twitch.tv"
    ],
    "Jogos": [
        "steam.com",
        "epicgames.com",
        "riotgames.com"
    ]
} 