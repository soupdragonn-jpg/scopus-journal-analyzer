@echo off
echo ========================================
echo SELENIUM CHROMEDRIVER TEST
echo ========================================
echo.

echo Проверявам Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ГРЕШКА: Python не е намерен!
    echo Моля инсталирайте Python от https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python е намерен
python --version

echo.
echo Проверявам Selenium...
python -c "import selenium; print('Selenium версия:', selenium.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ГРЕШКА: Selenium не е инсталиран!
    echo Инсталирам Selenium...
    pip install selenium
    if %errorlevel% neq 0 (
        echo ГРЕШКА: Не мога да инсталирам Selenium!
        pause
        exit /b 1
    )
)

echo ✓ Selenium е наличен

echo.
echo Проверявам ChromeDriver...
if exist chromedriver.exe (
    echo ✓ ChromeDriver намерен в текущата директория
) else (
    echo ⚠️ ChromeDriver не е намерен
    echo Опитвам автоматична инсталация...
    python install_chromedriver.py
    if %errorlevel% neq 0 (
        echo ГРЕШКА: Автоматичната инсталация неуспешна!
        echo Моля инсталирайте ChromeDriver ръчно от:
        echo https://chromedriver.chromium.org/
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo СТАРТИРАМ SELENIUM ТЕСТОВЕ
echo ========================================
echo.

echo Изберете тест:
echo 1. Прост тест (както поискахте)
echo 2. Подробен тест
echo 3. И двата теста

set /p choice="Вашият избор (1-3): "

if "%choice%"=="1" (
    echo.
    echo Стартирам прост тест...
    python simple_selenium_test.py
) else if "%choice%"=="2" (
    echo.
    echo Стартирам подробен тест...
    python test_selenium.py
) else if "%choice%"=="3" (
    echo.
    echo Стартирам прост тест...
    python simple_selenium_test.py
    echo.
    echo Стартирам подробен тест...
    python test_selenium.py
) else (
    echo Невалиден избор! Стартирам прост тест...
    python simple_selenium_test.py
)

echo.
echo ========================================
echo ТЕСТОВЕТЕ ЗАВЪРШИХА
echo ========================================
pause
