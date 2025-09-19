"""
Тест за проверка на Python настройката
Стартирайте този файл за да проверите дали всичко работи правилно
"""

import sys
import subprocess
import importlib

def test_python_version():
    """Проверява версията на Python"""
    print("🐍 Проверявам Python версия...")
    version = sys.version_info
    print(f"   Python версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✓ Python версията е подходяща (3.8+)")
        return True
    else:
        print("   ❌ Python версията е твърде стара (изисква се 3.8+)")
        return False

def test_pip():
    """Проверява дали pip работи"""
    print("\n📦 Проверявам pip...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ pip работи: {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ pip не работи: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Грешка при проверка на pip: {e}")
        return False

def test_required_packages():
    """Проверява дали всички необходими пакети са инсталирани"""
    print("\n📚 Проверявам необходимите пакети...")
    
    required_packages = [
        'flask',
        'requests', 
        'beautifulsoup4',
        'selenium',
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'plotly',
        'dash',
        'dash-bootstrap-components'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Някои пакети имат различни имена за импорт
            import_name = package
            if package == 'beautifulsoup4':
                import_name = 'bs4'
            elif package == 'dash-bootstrap-components':
                import_name = 'dash_bootstrap_components'
            
            importlib.import_module(import_name)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ❌ {package} - липсва")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   Липсват пакети: {', '.join(missing_packages)}")
        print("   Инсталирайте ги с: pip install -r requirements.txt")
        return False
    else:
        print("   ✓ Всички пакети са налични")
        return True

def test_selenium():
    """Проверява дали Selenium може да работи с Chrome"""
    print("\n🌐 Проверявам Selenium...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        print("   ✓ Selenium работи с Chrome")
        return True
        
    except Exception as e:
        print(f"   ⚠️ Selenium проблем: {e}")
        print("   ChromeDriver може да не е инсталиран правилно")
        print("   Приложението ще работи, но някои функции може да не са налични")
        return False

def test_flask():
    """Проверява дали Flask може да се стартира"""
    print("\n🚀 Проверявам Flask...")
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def test():
            return "Test OK"
        
        print("   ✓ Flask може да се стартира")
        return True
        
    except Exception as e:
        print(f"   ❌ Flask проблем: {e}")
        return False

def main():
    """Основна функция за тестване"""
    print("=" * 60)
    print("PYTHON SETUP TEST - SCOPUS JOURNAL ANALYZER")
    print("=" * 60)
    
    tests = [
        ("Python версия", test_python_version),
        ("pip", test_pip),
        ("Необходими пакети", test_required_packages),
        ("Selenium", test_selenium),
        ("Flask", test_flask)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Грешка в теста {test_name}: {e}")
            results.append((test_name, False))
    
    # Обобщение
    print("\n" + "=" * 60)
    print("ОБОБЩЕНИЕ НА РЕЗУЛТАТИТЕ")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ ПРОМИНА" if result else "❌ НЕУСПЕШЕН"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print(f"\nОбщо: {passed}/{total} теста преминаха")
    
    if passed == total:
        print("\n🎉 ВСИЧКО РАБОТИ ПРАВИЛНО!")
        print("Можете да стартирате приложението с: python run_app.py")
    elif passed >= total - 1:  # Ако само Selenium не работи
        print("\n⚠️ ПОЧТИ ВСИЧКО РАБОТИ!")
        print("Selenium има проблем, но приложението ще работи с ограничена функционалност")
        print("Можете да стартирате приложението с: python run_app.py")
    else:
        print("\n❌ ИМА ПРОБЛЕМИ С НАСТРОЙКАТА!")
        print("Моля следвайте инструкциите в PYTHON_SETUP_GUIDE.md")
    
    print("\nЗа помощ вижте: PYTHON_SETUP_GUIDE.md")

if __name__ == '__main__':
    main()

