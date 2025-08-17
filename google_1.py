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