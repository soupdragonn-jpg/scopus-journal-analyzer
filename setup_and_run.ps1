# Scopus Journal Analyzer - PowerShell Setup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SCOPUS JOURNAL ANALYZER - SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверка на Python
Write-Host "Проверявам Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python е намерен: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python не е намерен"
    }
} catch {
    Write-Host "ГРЕШКА: Python не е намерен!" -ForegroundColor Red
    Write-Host "Моля инсталирайте Python от https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "И маркирайте 'Add Python to PATH' при инсталация" -ForegroundColor Yellow
    Read-Host "Натиснете Enter за да излезете"
    exit 1
}

# Проверка на pip
Write-Host ""
Write-Host "Проверявам pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pip работи: $pipVersion" -ForegroundColor Green
    } else {
        # Опитваме с python -m pip
        $pipVersion = python -m pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ pip работи (чрез python -m pip): $pipVersion" -ForegroundColor Green
        } else {
            throw "pip не работи"
        }
    }
} catch {
    Write-Host "ГРЕШКА: pip не работи!" -ForegroundColor Red
    Read-Host "Натиснете Enter за да излезете"
    exit 1
}

# Създаване на виртуална среда
Write-Host ""
Write-Host "Създавам виртуална среда..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Виртуалната среда вече съществува" -ForegroundColor Yellow
} else {
    try {
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Виртуална среда създадена" -ForegroundColor Green
        } else {
            throw "Не мога да създам виртуална среда"
        }
    } catch {
        Write-Host "ГРЕШКА: Не мога да създам виртуална среда!" -ForegroundColor Red
        Read-Host "Натиснете Enter за да излезете"
        exit 1
    }
}

# Активиране на виртуална среда
Write-Host ""
Write-Host "Активирам виртуална среда..." -ForegroundColor Yellow
try {
    & "venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Виртуална среда активирана" -ForegroundColor Green
    } else {
        throw "Не мога да активирам виртуална среда"
    }
} catch {
    Write-Host "ГРЕШКА: Не мога да активирам виртуална среда!" -ForegroundColor Red
    Write-Host "Възможно е да трябва да разрешите изпълнение на скриптове:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Натиснете Enter за да излезете"
    exit 1
}

# Инсталиране на зависимости
Write-Host ""
Write-Host "Инсталирам зависимости..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Зависимости инсталирани" -ForegroundColor Green
    } else {
        # Опитваме с python -m pip
        python -m pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Зависимости инсталирани (чрез python -m pip)" -ForegroundColor Green
        } else {
            throw "Инсталацията неуспешна"
        }
    }
} catch {
    Write-Host "ГРЕШКА: Не мога да инсталирам зависимости!" -ForegroundColor Red
    Read-Host "Натиснете Enter за да излезете"
    exit 1
}

# Успешно завършване
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SETUP ЗАВЪРШЕН УСПЕШНО!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Стартирам приложението..." -ForegroundColor Yellow
Write-Host "Приложението ще се отвори на: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Натиснете Ctrl+C за да спрете" -ForegroundColor Yellow
Write-Host ""

# Стартиране на приложението
try {
    python run_app.py
} catch {
    Write-Host "Грешка при стартиране на приложението: $_" -ForegroundColor Red
}

Read-Host "Натиснете Enter за да излезете"
