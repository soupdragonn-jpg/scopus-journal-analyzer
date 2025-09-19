"""
Конфигурационен файл за Scopus Journal Analyzer
"""

import os
from dotenv import load_dotenv

# Зареждане на environment variables
load_dotenv()

class Config:
    """Основна конфигурация"""

    # Scopus API настройки
    SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY', '')
    SCOPUS_BASE_URL = 'https://api.elsevier.com/content/search/scopus'

    # Flask настройки
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Chrome Driver настройки
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '')

    # Logging настройки
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'scopus_analyzer.log')

    # Анализ настройки
    REQUEST_TIMEOUT = 30
    SELENIUM_WAIT_TIME = 3
    MAX_EDITORIAL_BOARD_SIZE = 50

    # Scopus критерии тегла
    SCOPUS_CRITERIA_WEIGHTS = {
        'content_quality': 0.25,
        'editorial_standards': 0.20,
        'peer_review_process': 0.20,
        'international_scope': 0.15,
        'technical_standards': 0.10,
        'accessibility': 0.10
    }

    # Ключови думи за анализ
    SCOPUS_KEYWORDS = [
        'peer review', 'editorial board', 'international', 'academic',
        'research', 'scholarly', 'scientific', 'journal', 'publication',
        'impact factor', 'citation', 'indexing', 'abstract', 'keywords',
        'doi', 'issn', 'isbn', 'open access', 'subscription'
    ]
