# Scopus Journal Readiness Analyzer

Приложение за анализ на готовността на научни списания за индексиране в базата данни Scopus.

## Описание

Това приложение анализира научни списания по URL адрес и оценява до каква степен са готови за кандидатиране за индексиране в Scopus. Анализът се основава на множество критерии, включително качество на съдържанието, редакционни стандарти, peer review процес, международен обхват, технически стандарти и достъпност.

## Функционалности

### 🔍 Анализ на списания
- **Web Scraping**: Автоматично извличане на данни от уебсайта на списанието
- **Selenium интеграция**: За динамично съдържание и JavaScript приложения
- **Множество източници**: Анализ на различни типове уебсайтове

### 📊 Критерии за оценка
1. **Качество на съдържанието** (25%)
   - Peer review процес
   - Редакционен съвет
   - ISSN и DOI наличност
   - Описание на списанието

2. **Редакционни стандарти** (20%)
   - Размер на редакционния съвет
   - Професионални титли
   - Международно представителство

3. **Peer Review процес** (20%)
   - Документиране на процеса
   - Тип рецензиране (double blind, single blind, open)
   - Времеви рамки

4. **Международен обхват** (15%)
   - Многоезичност
   - Международни автори
   - Open Access статус

5. **Технически стандарти** (10%)
   - ISSN номер
   - DOI система
   - HTTPS протокол
   - Структурирани данни

6. **Достъпност** (10%)
   - Open Access модел
   - Мобилна съвместимост
   - Честота на публикуване

### 📈 Визуализация
- **Интерактивни графики**: Radar chart за детайлна оценка
- **Цветово кодиране**: Визуална индикация на готовността
- **Детайлни отчети**: Подробна информация за всеки критерий

### 💡 Препоръки
- **Персонализирани съвети**: Конкретни препоръки за подобрение
- **Приоритизирани действия**: Съвети подредени по важност
- **Практични стъпки**: Изпълними препоръки за всеки критерий

## Инсталация

### 1. Клониране на репозиторията
```bash
git clone <repository-url>
cd scopus-journal-analyzer
```

### 2. Създаване на виртуална среда
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Инсталиране на зависимости
```bash
pip install -r requirements.txt
```

### 4. Настройка на Chrome Driver
- Изтеглете ChromeDriver от [официалния сайт](https://chromedriver.chromium.org/)
- Добавете пътя към ChromeDriver в environment variables или в `.env` файла

### 5. Конфигурация
Създайте `.env` файл в основната директория:
```env
SCOPUS_API_KEY=your_scopus_api_key_here
FLASK_DEBUG=True
CHROME_DRIVER_PATH=path/to/chromedriver
```

## Използване

### Стартиране на приложението
```bash
python app.py
```

Приложението ще се стартира на `http://localhost:5000`

### Анализ на списание
1. Отворете уеб браузъра и отидете на `http://localhost:5000`
2. Въведете URL адреса на списанието в полето за въвеждане
3. Натиснете "Анализирай списанието"
4. Изчакайте резултатите от анализа

### API използване
```python
import requests

url = "http://localhost:5000/analyze"
data = {"url": "https://example.com/journal"}

response = requests.post(url, json=data)
result = response.json()
```

## Структура на проекта

```
scopus-journal-analyzer/
├── app.py                 # Основно приложение
├── config.py             # Конфигурация
├── requirements.txt      # Python зависимости
├── README.md            # Документация
├── templates/
│   └── index.html       # HTML шаблон
└── .env                 # Environment variables (създайте сами)
```

## API Endpoints

### POST /analyze
Анализира списание по URL адрес.

**Параметри:**
- `url` (string): URL адрес на списанието

**Отговор:**
```json
{
  "journal_data": {
    "title": "Journal Title",
    "issn": "1234-5678",
    "editorial_board": [...],
    "peer_review_info": "...",
    ...
  },
  "readiness_analysis": {
    "total_score": 75.5,
    "readiness_level": "Средно готов",
    "detailed_scores": {...},
    "recommendations": [...]
  }
}
```

### GET /health
Health check endpoint.

**Отговор:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Конфигурация

### Scopus API
За пълна функционалност се препоръчва настройка на Scopus API ключ:
1. Регистрирайте се в [Elsevier Developer Portal](https://dev.elsevier.com/)
2. Получете API ключ
3. Добавете го в `.env` файла

### Chrome Driver
Selenium изисква ChromeDriver за автоматизация:
1. Изтеглете подходящата версия от [ChromeDriver](https://chromedriver.chromium.org/)
2. Добавете пътя в environment variables

## Ограничения

- **Rate Limiting**: Някои сайтове могат да блокират автоматизирани заявки
- **JavaScript**: Сложни JavaScript приложения могат да изискват допълнителна настройка
- **CAPTCHA**: Сайтове с CAPTCHA защита не могат да бъдат анализирани
- **Paywall**: Съдържание зад платена стена не е достъпно

## Развитие

### Добавяне на нови критерии
1. Разширете `SCOPUS_CRITERIA_WEIGHTS` в `config.py`
2. Добавете нова функция за анализ в `ScopusJournalAnalyzer`
3. Обновете `calculate_scopus_readiness` метода

### Подобряване на web scraping
1. Добавете нови селектори в `_extract_basic_info`
2. Разширете `_needs_selenium` логиката
3. Добавете специфична логика за различни платформи

## Лиценз

MIT License

## Поддръжка

За въпроси и проблеми, моля създайте issue в GitHub репозиторията.

## Версии

### v1.0.0
- Основна функционалност за анализ на списания
- Web scraping с BeautifulSoup и Selenium
- 6 основни критерия за оценка
- Интерактивен уеб интерфейс
- API endpoints
- Детайлни отчети и препоръки
