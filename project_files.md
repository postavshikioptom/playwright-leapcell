# Список файлов проекта Playwright-Leapcell

## Основные файлы проекта

### 1. main.py
Основной файл сервера приложения, реализующий веб-интерфейс и API для выполнения пользовательских скриптов Playwright.

### 2. requirements.txt
Файл зависимостей проекта, содержащий все необходимые Python библиотеки.

### 3. leapcell.yaml
Конфигурационный файл для платформы Leapcell, определяющий параметры развертывания приложения.

### 4. prepare_playwright_env.sh
Скрипт shell для подготовки окружения Playwright, включая установку браузера Chromium.

### 5. google_1.py
Пример пользовательского скрипта Playwright, демонстрирующий базовую функциональность.

### 6. README.md
Основная документация проекта, содержащая описание, инструкции по установке и использованию.

### 7. project_architecture.md
Документ с описанием архитектуры проекта и компонентов системы.

### 8. human_instruction.md
Инструкции для пользователя по развертыванию и использованию проекта.

### 9. static/style.css
Файл стилей для веб-интерфейса приложения.

## Детали содержимого файлов

### main.py
```python
import asyncio
from playwright.async_api import async_playwright
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import tempfile
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Playwright-Leapcell</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h1>Playwright-Leapcell Browser Automation</h1>
            <form action="/execute-script" method="post" enctype="multipart/form-data">
                <input type="file" name="script_file">
                <input type="submit" value="Выполнить скрипт">
            </form>
        </body>
    </html>
    """

@app.post("/execute-script")
async def execute_playwright_script(script_file: UploadFile = File(...)):
    try:
        # Сохраняем загруженный скрипт во временный файл
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            script_content = await script_file.read()
            f.write(script_content.decode())
            script_path = f.name

        # Выполняем скрипт
        logger.info(f"Выполнение скрипта: {script_file.filename}")
        process = await asyncio.create_subprocess_exec(
            "python", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        # Удаляем временный файл
        os.unlink(script_path)
        
        if process.returncode == 0:
            return {
                "status": "success",
                "output": stdout.decode(),
                "script_name": script_file.filename
            }
        else:
            raise HTTPException(status_code=500, detail=stderr.decode())
            
    except Exception as e:
        logger.error(f"Ошибка выполнения скрипта: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### requirements.txt
```
fastapi
uvicorn
playwright
```

### leapcell.yaml
```yaml
runtime: python3.9
build: |
  chmod +x prepare_playwright_env.sh
  ./prepare_playwright_env.sh
  pip install -r requirements.txt
start: python main.py
port: 8080
memory: 1024MB
```

### prepare_playwright_env.sh
```bash
#!/bin/bash
# Скрипт для подготовки окружения Playwright

echo "Установка Playwright и Chromium..."

# Установка Playwright
pip install playwright

# Установка браузера Chromium
playwright install chromium

echo "Playwright и Chromium успешно установлены!"
```

### google_1.py
```python
import asyncio
from playwright.async_api import async_playwright
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("Запуск скрипта google_1.py")
    
    async with async_playwright() as p:
        # Запуск браузера Chromium
        browser = await p.chromium.launch()
        
        # Создание новой страницы
        page = await browser.new_page()
        
        # Переход на сайт
        await page.goto("https://www.google.com")
        
        # Ожидание 10 секунд
        await page.wait_for_timeout(10000)
        
        # Запись в лог
        logger.info("GOOGLE - ГОТОВО")
        
        # Закрытие браузера
        await browser.close()
        
        logger.info("Скрипт завершен")

# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(main())
```

### README.md
```markdown
# Playwright-Leapcell

Проект для запуска пользовательских скриптов Playwright в браузере Chromium через веб-интерфейс, интегрированный с платформой Leapcell.

## Описание

Этот проект позволяет выполнять автоматизацию браузера Chromium с помощью пользовательских скриптов Playwright. Приложение предоставляет веб-интерфейс для загрузки и выполнения скриптов, а также API для программного взаимодействия.

## Особенности

- Выполнение пользовательских скриптов Playwright в браузере Chromium
- Веб-интерфейс для загрузки и выполнения скриптов
- API для программного взаимодействия
- Интеграция с платформой Leapcell
- Логирование выполнения скриптов

## Установка и запуск

Следуйте инструкциям в файле [human_instruction.md](human_instruction.md) для развертывания проекта на платформе Leapcell.

## Использование

1. Создайте скрипт Playwright с нужной вам функциональностью
2. Загрузите скрипт через веб-интерфейс или API
3. Дождитесь выполнения скрипта
4. Просмотрите результаты в логах

## Пример скрипта

Пример простого скрипта можно найти в файле [google_1.py](google_1.py).

## Архитектура

Подробное описание архитектуры проекта доступно в файле [project_architecture.md](project_architecture.md).
```

### static/style.css
```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}

h1 {
    color: #333;
    text-align: center;
}

form {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

input[type="file"] {
    margin-bottom: 10px;
}

input[type="submit"] {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

input[type="submit"]:hover {
    background-color: #45a049;
}