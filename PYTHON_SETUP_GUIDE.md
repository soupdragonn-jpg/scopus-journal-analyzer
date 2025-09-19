# Ръководство за настройка на Python - Windows

## 🚨 Проблемът, който имате

Когато пишете `pip install -r requirements.txt` в конзолата, получавате синтактична грешка. Това се случва, защото:

1. **Python не е инсталиран** или не е добавен към PATH
2. **pip не е наличен** или не работи правилно
3. **Грешка в командата** или кодиране

## ✅ Стъпка по стъпка решение

### Стъпка 1: Проверка дали Python е инсталиран

Отворете **Command Prompt** (cmd) или **PowerShell** и напишете:

```cmd
python --version
```

**Ако работи**, ще видите нещо като:
```
Python 3.9.7
```

**Ако НЕ работи**, ще видите:
```
'python' is not recognized as an internal or external command
```

### Стъпка 2: Ако Python НЕ е инсталиран

1. **Отидете на**: https://www.python.org/downloads/
2. **Изтеглете** най-новата версия на Python (3.8 или по-нова)
3. **ВАЖНО**: При инсталацията маркирайте "Add Python to PATH"
4. **Инсталирайте** Python
5. **Рестартирайте** конзолата

### Стъпка 3: Проверка на pip

След като Python е инсталиран, проверете pip:

```cmd
pip --version
```

**Ако работи**, ще видите нещо като:
```
pip 21.2.4 from C:\Python39\lib\site-packages\pip (python 3.9)
```

### Стъпка 4: Инсталиране на зависимости

Сега можете да инсталирате пакетите:

```cmd
pip install -r requirements.txt
```

## 🔧 Алтернативни начини

### Ако `python` не работи, опитайте:

```cmd
py --version
```

### Ако `pip` не работи, опитайте:

```cmd
python -m pip --version
```

### За инсталиране на пакети:

```cmd
python -m pip install -r requirements.txt
```

## 🐍 Създаване на виртуална среда (препоръчително)

Виртуалната среда изолира проекта и предотвратява конфликти:

### Създаване:
```cmd
python -m venv venv
```

### Активиране (Windows):
```cmd
venv\Scripts\activate
```

### Активиране (PowerShell):
```powershell
venv\Scripts\Activate.ps1
```

### След активиране, инсталирайте пакетите:
```cmd
pip install -r requirements.txt
```

## 🚀 Стартиране на приложението

След като всички пакети са инсталирани:

```cmd
python app.py
```

Или използвайте помощния скрипт:

```cmd
python run_app.py
```

## ❌ Често срещани грешки и решения

### Грешка 1: "python is not recognized"
**Решение**: Python не е инсталиран или не е в PATH
- Инсталирайте Python от python.org
- Маркирайте "Add Python to PATH" при инсталация

### Грешка 2: "pip is not recognized"
**Решение**: Използвайте `python -m pip` вместо `pip`

### Грешка 3: "Permission denied"
**Решение**: Стартирайте конзолата като администратор

### Грешка 4: "No module named 'flask'"
**Решение**: Пакетите не са инсталирани
- Активирайте виртуалната среда
- Инсталирайте пакетите: `pip install -r requirements.txt`

## 📋 Проверка на инсталацията

След инсталация, проверете дали всичко работи:

```cmd
python -c "import flask; print('Flask работи!')"
python -c "import requests; print('Requests работи!')"
python -c "import selenium; print('Selenium работи!')"
```

## 🎯 Бърз старт за вашия проект

1. **Отворете Command Prompt** в папката с проекта
2. **Създайте виртуална среда**:
   ```cmd
   python -m venv venv
   ```
3. **Активирайте я**:
   ```cmd
   venv\Scripts\activate
   ```
4. **Инсталирайте пакетите**:
   ```cmd
   pip install -r requirements.txt
   ```
5. **Стартирайте приложението**:
   ```cmd
   python run_app.py
   ```

## 📞 Ако все още има проблеми

1. **Проверете версията на Python**: `python --version`
2. **Проверете pip**: `pip --version`
3. **Опитайте с py**: `py --version`
4. **Рестартирайте конзолата**
5. **Проверете дали сте в правилната папка**

## 💡 Полезни команди

```cmd
# Проверка на Python
python --version
py --version

# Проверка на pip
pip --version
python -m pip --version

# Инсталиране на пакет
pip install package_name
python -m pip install package_name

# Инсталиране от requirements.txt
pip install -r requirements.txt
python -m pip install -r requirements.txt

# Списък на инсталирани пакети
pip list

# Деактивиране на виртуална среда
deactivate
```

---

**ВАЖНО**: Винаги използвайте виртуална среда за Python проекти!
