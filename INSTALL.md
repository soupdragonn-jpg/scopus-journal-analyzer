# Инструкции за инсталация - Scopus Journal Analyzer

## Бърза инсталация

### 1. Изтегляне на зависимости
```bash
pip install -r requirements.txt
```

### 2. Настройка на ChromeDriver
- Изтеглете ChromeDriver от [официалния сайт](https://chromedriver.chromium.org/)
- Добавете към PATH или създайте `.env` файл с пътя

### 3. Стартиране
```bash
python run_app.py
```

## Подробна инсталация

### Системни изисквания
- Python 3.8 или по-нова версия
- Google Chrome браузър
- ChromeDriver (за Selenium)
- Интернет връзка

### Стъпка 1: Подготовка на средата

#### Windows:
```cmd
# Създаване на виртуална среда
python -m venv venv
venv\Scripts\activate

# Инсталиране на зависимости
pip install -r requirements.txt
```

#### Linux/macOS:
```bash
# Създаване на виртуална среда
python3 -m venv venv
source venv/bin/activate

# Инсталиране на зависимости
pip install -r requirements.txt
```

### Стъпка 2: Настройка на ChromeDriver

#### Опция A: Автоматично (препоръчително)
```bash
# Инсталиране на webdriver-manager
pip install webdriver-manager
```

#### Опция B: Ръчно
1. Отидете на [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
2. Изтеглете версията, съответстваща на вашия Chrome браузър
3. Разархивирайте и добавете към PATH

### Стъпка 3: Конфигурация

Създайте `.env` файл в основната директория:
```env
# Scopus API Configuration (опционално)
SCOPUS_API_KEY=your_scopus_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Chrome Driver Configuration
CHROME_DRIVER_PATH=path/to/chromedriver

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=scopus_analyzer.log
```

### Стъпка 4: Тестване

```bash
# Стартиране на тестовете
python test_analyzer.py
```

### Стъпка 5: Стартиране на приложението

```bash
# Стартиране с помощен скрипт
python run_app.py

# Или директно
python app.py
```

Приложението ще се отвори на: `http://localhost:5000`

## Настройка на Scopus API (опционално)

За пълна функционалност се препоръчва настройка на Scopus API:

1. Регистрирайте се в [Elsevier Developer Portal](https://dev.elsevier.com/)
2. Създайте ново приложение
3. Получете API ключ
4. Добавете го в `.env` файла

## Решаване на проблеми

### ChromeDriver грешки
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Решение:** Инсталирайте ChromeDriver или използвайте webdriver-manager

### Import грешки
```
ModuleNotFoundError: No module named 'flask'
```
**Решение:** Активирайте виртуалната среда и инсталирайте зависимостите

### Port зает
```
OSError: [Errno 98] Address already in use
```
**Решение:** Сменете порта в `app.py` или спрете другия процес

### SSL грешки
```
SSL: CERTIFICATE_VERIFY_FAILED
```
**Решение:** Обновете сертификатите или използвайте HTTP вместо HTTPS

## Структура на проекта

```
scopus-journal-analyzer/
├── app.py                 # Основно приложение
├── config.py             # Конфигурация
├── scopus_api.py         # Scopus API интеграция
├── test_analyzer.py      # Тестове
├── run_app.py           # Помощен скрипт за стартиране
├── requirements.txt     # Python зависимости
├── README.md           # Документация
├── INSTALL.md          # Инструкции за инсталация
├── templates/
│   └── index.html      # HTML шаблон
└── .env               # Environment variables (създайте сами)
```

## Поддръжка

За въпроси и проблеми:
1. Проверете логовете в `scopus_analyzer.log`
2. Стартирайте тестовете: `python test_analyzer.py`
3. Проверете дали всички зависимости са инсталирани
4. Уверете се, че ChromeDriver работи правилно

## Лиценз

MIT License - свободно за използване и модификация.
