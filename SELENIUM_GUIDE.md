# 🚀 Selenium ChromeDriver - Ръководство

## 🎯 Какво направих вместо вас

Създадох няколко файла, които правят точно това, което поискахте:

### 📁 Създадени файлове:

1. **`simple_selenium_test.py`** - Точно вашия код, адаптиран за Windows
2. **`test_selenium.py`** - Подробен тест с много функции
3. **`install_chromedriver.py`** - Автоматичен инсталатор за ChromeDriver
4. **`test_selenium.bat`** - Batch файл за лесно стартиране

## 🚀 Най-лесният начин да тествате

**Двойно кликнете на `test_selenium.bat`** - този файл ще направи всичко автоматично!

## 📋 Ръчно стартиране

### Стъпка 1: Инсталирайте ChromeDriver
```cmd
python install_chromedriver.py
```

### Стъпка 2: Стартирайте теста
```cmd
python simple_selenium_test.py
```

## 🔍 Какво прави всеки файл

### `simple_selenium_test.py`
- **Точно вашия код**, адаптиран за Windows
- Автоматично намира ChromeDriver
- Отваря Google и изчаква 5 секунди
- Показва заглавието на страницата

### `test_selenium.py`
- **Подробен тест** с много функции
- Тества търсене в Google
- Тества навигация (назад/напред)
- Може да се стартира с или без GUI

### `install_chromedriver.py`
- **Автоматично изтегля** ChromeDriver
- Намира версията на вашия Chrome
- Изтегля съответната версия на ChromeDriver
- Тества дали работи правилно

## 🎯 Вашият код (адаптиран)

Ето как изглежда вашият код в `simple_selenium_test.py`:

```python
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def find_chromedriver():
    # Автоматично намира ChromeDriver
    if os.path.exists('chromedriver.exe'):
        return './chromedriver.exe'
    # ... други начини за намиране

def main():
    # Намираме ChromeDriver
    chromedriver_path = find_chromedriver()
    
    if chromedriver_path:
        service = Service(chromedriver_path)
    else:
        service = Service()  # От PATH
    
    try:
        # Стартираме ChromeDriver
        service.start()
        
        # Създаваме WebDriver
        driver = webdriver.Remote(service.service_url)
        
        # Отваряме Google
        driver.get('http://www.google.com/')
        
        # Изчакваме 5 секунди
        time.sleep(5)
        
        print("✅ Тестът завърши успешно!")
        print(f"📊 Заглавие: {driver.title}")
        
    except Exception as e:
        print(f"❌ Грешка: {e}")
        
    finally:
        # Затваряме всичко
        if 'driver' in locals():
            driver.quit()
        if service:
            service.stop()
```

## 🔧 Решаване на проблеми

### Проблем 1: "ChromeDriver not found"
**Решение**: Стартирайте `python install_chromedriver.py`

### Проблем 2: "Chrome not found"
**Решение**: Инсталирайте Google Chrome от https://www.google.com/chrome/

### Проблем 3: "Permission denied"
**Решение**: Стартирайте конзолата като администратор

### Проблем 4: "Selenium not installed"
**Решение**: `pip install selenium`

## 🎉 След като всичко работи

Когато Selenium тестовете преминат успешно, можете да:

1. **Стартирате основното приложение**:
   ```cmd
   python run_app.py
   ```

2. **Тествате Scopus анализатора**:
   ```cmd
   python demo.py
   ```

3. **Използвате Selenium в собствени проекти**

## 📞 За помощ

1. **Стартирайте автоматичния тест**: `test_selenium.bat`
2. **Проверете дали Chrome е инсталиран**
3. **Инсталирайте ChromeDriver**: `python install_chromedriver.py`
4. **Стартирайте простия тест**: `python simple_selenium_test.py`

---

**💡 Съвет**: Винаги използвайте виртуална среда за Python проекти!

