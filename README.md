# Page Analyzer

 — веб-приложение на Flask, которое анализирует указанные страницы на SEO-пригодность. Проверяется доступность сайта, извлекаются теги h1, title и meta description.


### Hexlet tests and linter status:
[![Actions Status](https://github.com/buna-p/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/buna-p/python-project-83/actions)


## Демонстрационный сайт
https://python-project-83-97v9.onrender.com


**Возможности:**

- Валидация URL – проверка корректности введенных адресов.
- Мониторинг доступности – отслеживание кода ответа сервера.
- SEO-анализ – проверка основных метаданных страницы.
- История проверок – хранение и просмотр предыдущих проверок.

## Работа

**Установка:**
1. Клонируйте репозиторий командой *git clone*.
2. Установите пакет командой *make install*.
3. Создайте базу данных командой *createdb page_analyzer*.
4. Настройте переменные окружения.
5. Примените миграции командой *psql -d $DATABASE_URL -f database.sql*.
6. Запустите приложение командой *make dev*.
