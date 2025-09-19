# 🚀 Бърз старт - Scopus Journal Analyzer

## ❌ Проблемът, който имате

Когато пишете `pip install -r requirements.txt` в конзолата, получавате синтаксична грешка.

## ✅ Решение (3 стъпки)

### Стъпка 1: Проверете Python
Отворете **Command Prompt** и напишете:
```cmd
python --version
```

**Ако НЕ работи**, инсталирайте Python:
1. Отидете на: https://www.python.org/downloads/
2. Изтеглете Python 3.8+
3. **ВАЖНО**: Маркирайте "Add Python to PATH"
4. Инсталирайте и рестартирайте конзолата

### Стъпка 2: Автоматично настройване
**Двойно кликнете** на един от тези файлове:

- **`setup_and_run.bat`** (за Command Prompt)
- **`setup_and_run.ps1`** (за PowerShell)

Тези файлове ще направят всичко автоматично!

### Стъпка 3: Ръчно настройване (ако автоматичното не работи)

```cmd
# 1. Създайте виртуална среда
python -m venv venv

# 2. Активирайте я
venv\Scripts\activate

# 3. Инсталирайте пакетите
pip install -r requirements.txt

# 4. Стартирайте приложението
python run_app.py
```

## 🧪 Проверка дали всичко работи

Стартирайте теста:
```cmd
python test_python_setup.py
```

## 🌐 Стартиране на приложението

След като всичко е настроено:
```cmd
python run_app.py
```

Приложението ще се отвори на: **http://localhost:5000**

## ❓ Ако все още има проблеми

### Проблем 1: "python is not recognized"
**Решение**: Python не е инсталиран или не е в PATH
- Инсталирайте Python от python.org
- Маркирайте "Add Python to PATH"

### Проблем 2: "pip is not recognized"  
**Решение**: Използвайте `python -m pip` вместо `pip`

### Проблем 3: PowerShell грешки
**Решение**: Разрешете изпълнение на скриптове:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Проблем 4: ChromeDriver грешки
**Решение**: Приложението ще работи, но някои функции може да не са налични

## 📞 За помощ

1. Проверете `PYTHON_SETUP_GUIDE.md` за подробни инструкции
2. Стартирайте `python test_python_setup.py` за диагностика
3. Използвайте автоматичните скриптове `setup_and_run.bat` или `setup_and_run.ps1`

---

**💡 Съвет**: Винаги използвайте виртуална среда за Python проекти!

