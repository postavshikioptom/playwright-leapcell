import asyncio
from playwright.async_api import async_playwright
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        
        # Выводим логи выполнения скрипта в логи основного приложения
        if stdout:
            logger.info(f"STDOUT скрипта {script_file.filename}:\n{stdout.decode()}")
        if stderr:
            logger.info(f"STDERR скрипта {script_file.filename}:\n{stderr.decode()}")
        
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

# Endpoint'ы для проверки здоровья, запрашиваемые инфраструктурой Leapcell
@app.get("/kaithhealthcheck")
async def kaith_health_check():
    return {"status": "ok"}

@app.get("/kaithheathcheck")
async def kaith_health_check_typo():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)