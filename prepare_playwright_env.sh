#!/bin/bash
# Скрипт для подготовки окружения Playwright

echo "Установка системных зависимостей для Playwright..."
apt-get update
apt-get install -y \
  libglib2.0-0 \
  libnss3 \
  libnspr4 \
  libdbus-1-3 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libxcb1 \
  libxkbcommon0 \
  libexpat1 \
  libx11-6 \
  libxcomposite1 \
  libxdamage1 \
  libxext6 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libasound2

echo "Проверка установленных библиотек..."
ldconfig -p | grep -E "libglib|libnss|libnspr|libdbus|libatk|libcups|libdrm|libxcb|libxkbcommon|libexpat|libx11|libxcomposite|libxdamage|libxext|libxfixes|libxrandr|libgbm|libasound"

echo "Установка Playwright и Chromium..."

# Установка Playwright
pip install playwright

# Установка браузера Chromium
playwright install chromium

# Проверка установки Chromium
echo "Проверка установки Chromium..."
playwright install-deps
playwright show-trace

echo "Playwright и Chromium успешно установлены!"