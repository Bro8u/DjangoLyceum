# Проект Django "Lyceum"

Это учебный проект, созданный на Django 4.2.*, с тремя приложениями: `homepage`, `catalog` и `about`.

## Требования

- Python 3.10+
- pip (последняя версия)
- Виртуальная среда (рекомендуется)

## Установка и настройка

1. Клонируйте репозиторий:

    ```bash
    git clone <ссылка на ваш репозиторий>
    ```

2. Перейдите в директорию проекта:

    ```bash
    cd <название директории проекта>
    ```

3. Создайте и активируйте виртуальную среду:

    - **Linux/Mac OS**:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    - **Windows**:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

4. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

5. Выполните миграции базы данных:

    ```bash
    python manage.py migrate
    ```

6. Создайте суперпользователя для админ-панели:

    ```bash
    python manage.py createsuperuser
    ```

7. Соберите статические файлы (опционально для dev-режима, но требуется для production):

    ```bash
    python manage.py collectstatic
    ```

## Запуск проекта в dev-режиме

Для запуска проекта в режиме разработки (development mode) выполните следующую команду:

```bash
python manage.py runserver
