"""
Скрипт за стартиране на Scopus Journal Analyzer
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Проверява дали всички зависимости са инсталирани"""
    print("Проверявам зависимости...")
    
    required_packages = [
        'flask', 'requests', 'beautifulsoup4', 'selenium', 
        'pandas', 'numpy', 'scikit-learn', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - липсва")
    
    if missing_packages:
        print(f"\nЛипсват пакети: {', '.join(missing_packages)}")
        print("Инсталирайте ги с: pip install -r requirements.txt")
        return False
    
    print("Всички зависимости са налични!")
    return True

def check_chrome_driver():
    """Проверява дали ChromeDriver е наличен"""
    print("\nПроверявам ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        print("✓ ChromeDriver работи правилно")
        return True
        
    except Exception as e:
        print(f"✗ ChromeDriver проблем: {e}")
        print("\nЗа да инсталирате ChromeDriver:")
        print("1. Изтеглете от: https://chromedriver.chromium.org/")
        print("2. Добавете към PATH или задайте CHROME_DRIVER_PATH в .env файла")
        return False

def create_env_file():
    """Създава .env файл ако не съществува"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("\nСъздавам .env файл...")
        
        env_content = """# Scopus API Configuration
SCOPUS_API_KEY=your_scopus_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Chrome Driver Configuration (optional)
CHROME_DRIVER_PATH=path/to/chromedriver

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=scopus_analyzer.log
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✓ .env файл създаден")
        print("Моля редактирайте го и добавете вашия Scopus API ключ")
    else:
        print("✓ .env файл съществува")

def run_tests():
    """Стартира тестовете"""
    print("\nСтартирам тестове...")
    
    try:
        result = subprocess.run([sys.executable, 'test_analyzer.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Всички тестове преминаха успешно")
            return True
        else:
            print("✗ Някои тестове не преминаха")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Грешка при стартиране на тестовете: {e}")
        return False

def start_application():
    """Стартира приложението"""
    print("\nСтартирам Scopus Journal Analyzer...")
    print("Приложението ще се отвори на: http://localhost:5000")
    print("Натиснете Ctrl+C за да спрете приложението")
    
    try:
        # Стартираме приложението
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\nПриложението е спряно от потребителя")
    except Exception as e:
        print(f"Грешка при стартиране на приложението: {e}")

def main():
    """Основна функция"""
    print("=" * 60)
    print("SCOPUS JOURNAL READINESS ANALYZER")
    print("=" * 60)
    
    # Проверяваме зависимостите
    if not check_dependencies():
        print("\nМоля инсталирайте липсващите пакети преди да продължите")
        return
    
    # Проверяваме ChromeDriver
    chrome_driver_ok = check_chrome_driver()
    if not chrome_driver_ok:
        print("\nВНИМАНИЕ: ChromeDriver не работи правилно.")
        print("Някои функции може да не работят.")
        response = input("Искате ли да продължите? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Създаваме .env файл
    create_env_file()
    
    # Питаме дали да стартираме тестовете
    run_tests_choice = input("\nИскате ли да стартирате тестовете? (y/n): ")
    if run_tests_choice.lower() == 'y':
        if not run_tests():
            print("\nВНИМАНИЕ: Някои тестове не преминаха.")
            response = input("Искате ли да продължите? (y/n): ")
            if response.lower() != 'y':
                return
    
    # Стартираме приложението
    start_application()

if __name__ == '__main__':
    main()

