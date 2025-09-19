"""
Тест за Selenium и ChromeDriver
Проверява дали Selenium може да работи с Chrome браузър
"""

import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_chromedriver():
    """Опитва се да намери ChromeDriver автоматично"""
    possible_paths = [
        # В текущата директория
        './chromedriver.exe',
        './chromedriver',
        
        # В PATH
        'chromedriver.exe',
        'chromedriver',
        
        # Често срещани места в Windows
        'C:/Program Files/Google/Chrome/Application/chromedriver.exe',
        'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',
        'C:/Users/{}/AppData/Local/Google/Chrome/Application/chromedriver.exe'.format(os.getenv('USERNAME', '')),
        
        # В папката на проекта
        './drivers/chromedriver.exe',
        './drivers/chromedriver',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Намерен ChromeDriver: {path}")
            return path
    
    return None

def test_selenium_basic():
    """Основен тест на Selenium"""
    print("=" * 60)
    print("SELENIUM CHROMEDRIVER TEST")
    print("=" * 60)
    
    # Настройки за Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Без GUI за по-бързо тестване
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    
    try:
        print("🔍 Търся ChromeDriver...")
        chromedriver_path = find_chromedriver()
        
        if chromedriver_path:
            print(f"📍 Използвам ChromeDriver: {chromedriver_path}")
            service = Service(chromedriver_path)
        else:
            print("⚠️ ChromeDriver не е намерен в файловата система")
            print("🔄 Опитвам да използвам ChromeDriver от PATH...")
            service = Service()  # Опитва се да намери в PATH
        
        print("🚀 Стартирам Chrome браузър...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome браузърът е стартиран успешно!")
        
        # Тест 1: Отваряне на Google
        print("\n📄 Тест 1: Отваряне на Google...")
        driver.get('https://www.google.com/')
        
        # Проверяваме дали страницата се е заредила
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "q")))
        
        print("✅ Google се отвори успешно!")
        print(f"📊 Заглавие на страницата: {driver.title}")
        
        # Тест 2: Търсене
        print("\n🔍 Тест 2: Търсене в Google...")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium Python test")
        search_box.submit()
        
        # Изчакваме резултатите
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        print("✅ Търсенето работи успешно!")
        
        # Тест 3: Проверка на резултатите
        print("\n📋 Тест 3: Проверка на резултатите...")
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        print(f"✅ Намерени {len(results)} резултата от търсенето")
        
        # Тест 4: Навигация
        print("\n🔄 Тест 4: Навигация...")
        driver.back()
        time.sleep(1)
        driver.forward()
        time.sleep(1)
        print("✅ Навигацията работи успешно!")
        
        print("\n🎉 ВСИЧКИ ТЕСТОВЕ ПРЕМИНАХА УСПЕШНО!")
        print("Selenium и ChromeDriver работят перфектно!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ГРЕШКА: {e}")
        print("\n🔧 Възможни решения:")
        print("1. Инсталирайте ChromeDriver от: https://chromedriver.chromium.org/")
        print("2. Добавете ChromeDriver към PATH")
        print("3. Поставете chromedriver.exe в папката на проекта")
        print("4. Проверете дали Google Chrome е инсталиран")
        
        return False
        
    finally:
        if driver:
            print("\n🔄 Затварям браузъра...")
            driver.quit()
            print("✅ Браузърът е затворен")

def test_selenium_with_gui():
    """Тест на Selenium с GUI (за визуална проверка)"""
    print("\n" + "=" * 60)
    print("SELENIUM GUI TEST (С ВИЗУАЛЕН ИНТЕРФЕЙС)")
    print("=" * 60)
    
    # Настройки за Chrome с GUI
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1200,800')
    
    driver = None
    
    try:
        print("🔍 Търся ChromeDriver...")
        chromedriver_path = find_chromedriver()
        
        if chromedriver_path:
            service = Service(chromedriver_path)
        else:
            service = Service()
        
        print("🚀 Стартирам Chrome браузър с GUI...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome браузърът е стартиран с GUI!")
        
        # Отваряме Google
        print("📄 Отварям Google...")
        driver.get('https://www.google.com/')
        
        print("⏱️ Браузърът ще остане отворен 10 секунди...")
        print("👀 Можете да видите как работи Selenium!")
        
        time.sleep(10)
        
        print("✅ GUI тестът завърши успешно!")
        return True
        
    except Exception as e:
        print(f"❌ GUI тест неуспешен: {e}")
        return False
        
    finally:
        if driver:
            print("🔄 Затварям браузъра...")
            driver.quit()

def main():
    """Основна функция"""
    print("SELENIUM CHROMEDRIVER TESTER")
    print("Този скрипт тества дали Selenium работи с ChromeDriver")
    print()
    
    # Проверяваме дали Selenium е инсталиран
    try:
        import selenium
        print(f"✓ Selenium версия: {selenium.__version__}")
    except ImportError:
        print("❌ Selenium не е инсталиран!")
        print("Инсталирайте го с: pip install selenium")
        return
    
    # Проверяваме дали Chrome е инсталиран
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✓ Google Chrome намерен: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("⚠️ Google Chrome не е намерен в стандартните места")
        print("Моля инсталирайте Google Chrome от: https://www.google.com/chrome/")
    
    print()
    
    # Питаме потребителя какъв тест иска
    print("Изберете тип тест:")
    print("1. Бърз тест (без GUI)")
    print("2. GUI тест (с визуален интерфейс)")
    print("3. И двата теста")
    
    choice = input("\nВашият избор (1-3): ").strip()
    
    if choice == "1":
        test_selenium_basic()
    elif choice == "2":
        test_selenium_with_gui()
    elif choice == "3":
        test_selenium_basic()
        test_selenium_with_gui()
    else:
        print("Невалиден избор! Стартирам бърз тест...")
        test_selenium_basic()
    
    print("\n" + "=" * 60)
    print("ТЕСТЪТ ЗАВЪРШИ")
    print("=" * 60)

if __name__ == "__main__":
    main()
