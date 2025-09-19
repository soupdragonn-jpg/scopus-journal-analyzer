"""
Автоматичен инсталатор за ChromeDriver
Изтегля и настройва ChromeDriver автоматично
"""

import os
import sys
import requests
import zipfile
import json
import subprocess
from pathlib import Path

def get_chrome_version():
    """Получава версията на инсталирания Chrome"""
    try:
        # Windows команда за получаване на версията на Chrome
        result = subprocess.run([
            'reg', 'query', 
            'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', 
            '/v', 'version'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            version_line = result.stdout.strip().split('\n')[-1]
            version = version_line.split()[-1]
            return version
    except:
        pass
    
    # Алтернативен начин
    try:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                result = subprocess.run([chrome_path, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip().split()[-1]
                    return version
    except:
        pass
    
    return None

def get_chromedriver_version(chrome_version):
    """Получава съответната версия на ChromeDriver"""
    try:
        # API за получаване на версията на ChromeDriver
        major_version = chrome_version.split('.')[0]
        
        # Опитваме да получим последната стабилна версия
        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    return None

def download_chromedriver(version):
    """Изтегля ChromeDriver"""
    try:
        # Определяме архитектурата
        if sys.maxsize > 2**32:
            platform = "win32"  # 64-bit
        else:
            platform = "win32"  # 32-bit
        
        # URL за изтегляне
        url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform}.zip"
        
        print(f"📥 Изтеглям ChromeDriver версия {version}...")
        print(f"🔗 URL: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Запазваме ZIP файла
        zip_path = "chromedriver.zip"
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        print("✅ ChromeDriver изтеглен успешно!")
        return zip_path
        
    except Exception as e:
        print(f"❌ Грешка при изтегляне: {e}")
        return None

def extract_chromedriver(zip_path):
    """Извлича ChromeDriver от ZIP файла"""
    try:
        print("📦 Извличам ChromeDriver...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        # Проверяваме дали файлът е извлечен
        if os.path.exists('chromedriver.exe'):
            print("✅ ChromeDriver извлечен успешно!")
            return True
        else:
            print("❌ ChromeDriver не е намерен в архива!")
            return False
            
    except Exception as e:
        print(f"❌ Грешка при извличане: {e}")
        return False
    finally:
        # Изтриваме ZIP файла
        try:
            os.remove(zip_path)
        except:
            pass

def test_chromedriver():
    """Тества дали ChromeDriver работи"""
    try:
        print("🧪 Тествам ChromeDriver...")
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.google.com')
        driver.quit()
        
        print("✅ ChromeDriver работи перфектно!")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver тест неуспешен: {e}")
        return False

def main():
    """Основна функция"""
    print("=" * 60)
    print("CHROMEDRIVER АВТОМАТИЧЕН ИНСТАЛАТОР")
    print("=" * 60)
    
    # Проверяваме дали ChromeDriver вече съществува
    if os.path.exists('chromedriver.exe'):
        print("✅ ChromeDriver вече съществува в текущата директория!")
        
        # Тестваме дали работи
        if test_chromedriver():
            print("🎉 ChromeDriver работи отлично!")
            return
        else:
            print("⚠️ ChromeDriver не работи, ще го преинсталирам...")
    
    # Получаваме версията на Chrome
    print("🔍 Търся версията на Google Chrome...")
    chrome_version = get_chrome_version()
    
    if not chrome_version:
        print("❌ Не мога да намеря Google Chrome!")
        print("Моля инсталирайте Google Chrome от: https://www.google.com/chrome/")
        return
    
    print(f"✅ Намерен Google Chrome версия: {chrome_version}")
    
    # Получаваме версията на ChromeDriver
    print("🔍 Търся съответната версия на ChromeDriver...")
    chromedriver_version = get_chromedriver_version(chrome_version)
    
    if not chromedriver_version:
        print("❌ Не мога да намеря съответната версия на ChromeDriver!")
        print("Моля инсталирайте ChromeDriver ръчно от: https://chromedriver.chromium.org/")
        return
    
    print(f"✅ Намерена версия на ChromeDriver: {chromedriver_version}")
    
    # Изтегляме ChromeDriver
    zip_path = download_chromedriver(chromedriver_version)
    if not zip_path:
        return
    
    # Извличаме ChromeDriver
    if not extract_chromedriver(zip_path):
        return
    
    # Тестваме ChromeDriver
    if test_chromedriver():
        print("\n🎉 CHROMEDRIVER ИНСТАЛИРАН УСПЕШНО!")
        print("Сега можете да използвате Selenium!")
        
        print("\n📋 Следващи стъпки:")
        print("1. Стартирайте: python simple_selenium_test.py")
        print("2. Или: python test_selenium.py")
        print("3. Или: python run_app.py")
    else:
        print("\n❌ ChromeDriver е инсталиран, но не работи правилно!")
        print("Моля проверете дали Google Chrome е инсталиран правилно.")

if __name__ == "__main__":
    main()
