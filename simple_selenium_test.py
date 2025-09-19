"""
Прост тест на Selenium - точно както поискахте
Адаптиран за Windows и автоматично откриване на ChromeDriver
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def find_chromedriver():
    """Намира ChromeDriver автоматично"""
    # Първо проверяваме в текущата директория
    if os.path.exists('chromedriver.exe'):
        return './chromedriver.exe'
    if os.path.exists('chromedriver'):
        return './chromedriver'
    
    # Проверяваме в PATH
    try:
        from shutil import which
        chromedriver_path = which('chromedriver.exe') or which('chromedriver')
        if chromedriver_path:
            return chromedriver_path
    except:
        pass
    
    return None

def main():
    """Основен тест - точно както поискахте"""
    print("🚀 Стартирам Selenium тест...")
    
    # Намираме ChromeDriver
    chromedriver_path = find_chromedriver()
    
    if chromedriver_path:
        print(f"📍 Използвам ChromeDriver: {chromedriver_path}")
        service = Service(chromedriver_path)
    else:
        print("⚠️ ChromeDriver не е намерен, опитвам от PATH...")
        service = Service()  # Опитва се да намери в PATH
    
    try:
        # Стартираме ChromeDriver
        print("🔄 Стартирам ChromeDriver...")
        service.start()
        
        # Създаваме WebDriver
        print("🌐 Създавам WebDriver...")
        driver = webdriver.Remote(service.service_url)
        
        # Отваряме Google
        print("📄 Отварям Google...")
        driver.get('http://www.google.com/')
        
        # Изчакваме 5 секунди
        print("⏱️ Изчаквам 5 секунди...")
        time.sleep(5)
        
        print("✅ Тестът завърши успешно!")
        print(f"📊 Заглавие на страницата: {driver.title}")
        
    except Exception as e:
        print(f"❌ Грешка: {e}")
        print("\n🔧 Възможни решения:")
        print("1. Инсталирайте ChromeDriver от: https://chromedriver.chromium.org/")
        print("2. Поставете chromedriver.exe в папката на проекта")
        print("3. Добавете ChromeDriver към PATH")
        
    finally:
        # Затваряме всичко
        try:
            if 'driver' in locals():
                print("🔄 Затварям браузъра...")
                driver.quit()
            
            if service:
                print("🔄 Спирам ChromeDriver...")
                service.stop()
                
        except Exception as e:
            print(f"⚠️ Грешка при затваряне: {e}")
        
        print("✅ Тестът завърши!")

if __name__ == "__main__":
    main()

