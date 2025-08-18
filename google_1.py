import asyncio
from playwright.async_api import async_playwright
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("Запуск скрипта google_1.py")
    
    async with async_playwright() as p:
        logger.info("Playwright инициализирован")
        
        # Запуск браузера Chromium с дополнительными параметрами
        logger.info("Попытка запуска браузера Chromium")
        browser = await p.chromium.launch(headless=True)
        logger.info("Браузер Chromium успешно запущен")
        
        # Создание новой страницы
        logger.info("Попытка создания новой страницы")
        page = await browser.new_page()
        logger.info("Новая страница успешно создана")
        
        # Переход на сайт
        logger.info("Попытка перехода на сайт https://www.google.com")
        await page.goto("https://www.google.com")
        logger.info("Успешно перешли на сайт https://www.google.com")
        
        # Ожидание 10 секунд
        logger.info("Ожидание 10 секунд")
        await page.wait_for_timeout(10000)
        logger.info("Ожидание завершено")
        
        # Запись в лог
        logger.info("GOOGLE - ГОТОВО")
        
        # Закрытие браузера
        logger.info("Попытка закрытия браузера")
        await browser.close()
        logger.info("Браузер успешно закрыт")
        
        logger.info("Скрипт завершен")

# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(main())