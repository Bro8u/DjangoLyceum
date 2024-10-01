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
    
5. Создайте файл .env в корне проекта и добавьте туда переменные окружения:

    SECRET_KEY="django-insecure-+9rpfah-dg7^9s0=w&p_bdy!yhfns^thwb0d@prthiqc91gs_@"
    DEBUG=True

6. Создайте суперпользователя для админ-панели:

    ```bash
    python manage.py createsuperuser
    ```
    
## Запуск проекта в dev-режиме

Для запуска проекта в режиме разработки (development mode) выполните следующую команду:

```bash
python manage.py runserver
