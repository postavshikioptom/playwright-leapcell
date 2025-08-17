#!/bin/bash
# Скрипт для подготовки окружения Playwright

echo "Установка Playwright и Chromium..."

# Установка Playwright
pip install playwright

# Установка браузера Chromium
playwright install chromium

echo "Playwright и Chromium успешно установлены!"