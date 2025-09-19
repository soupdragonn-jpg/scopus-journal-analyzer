@echo off
echo ========================================
echo SCOPUS JOURNAL ANALYZER - SETUP
echo ========================================
echo.

echo Проверявам Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ГРЕШКА: Python не е намерен!
    echo Моля инсталирайте Python от https://www.python.org/downloads/
    echo И маркирайте "Add Python to PATH" при инсталация
    pause
    exit /b 1
)

echo ✓ Python е намерен
python --version

echo.
echo Проверявам pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ГРЕШКА: pip не е намерен!
    echo Опитвам с python -m pip...
    python -m pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ГРЕШКА: pip не работи!
        pause
        exit /b 1
    )
)

echo ✓ pip работи

echo.
echo Създавам виртуална среда...
if exist venv (
    echo Виртуалната среда вече съществува
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ГРЕШКА: Не мога да създам виртуална среда!
        pause
        exit /b 1
    )
    echo ✓ Виртуална среда създадена
)

echo.
echo Активирам виртуална среда...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ГРЕШКА: Не мога да активирам виртуална среда!
    pause
    exit /b 1
)

echo ✓ Виртуална среда активирана

echo.
echo Инсталирам зависимости...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ГРЕШКА: Не мога да инсталирам зависимости!
    echo Опитвам с python -m pip...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ГРЕШКА: Инсталацията неуспешна!
        pause
        exit /b 1
    )
)

echo ✓ Зависимости инсталирани

echo.
echo ========================================
echo SETUP ЗАВЪРШЕН УСПЕШНО!
echo ========================================
echo.
echo Стартирам приложението...
echo Приложението ще се отвори на: http://localhost:5000
echo Натиснете Ctrl+C за да спрете
echo.

python run_app.py

pause
