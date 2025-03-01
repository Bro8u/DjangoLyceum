# Проект Django "Lyceum"
![Pipeline Status](https://gitlab.crja72.ru/django/2024/autumn/course/students/286724-betttttt-course-1187/badges/main/pipeline.svg)

Это учебный проект, созданный на Django 4.2.*, с тремя приложениями: `homepage`, `catalog` и `about`.

## Требования

- Python 3.10+
- pip (последняя версия)
- Виртуальная среда (рекомендуется)

## Установка и настройка

1. Клонируйте репозиторий:

    ```bash
    git clone git@gitlab.crja72.ru:django/2024/autumn/course/students/286724-betttttt-course-1187.git
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
        python3 -m venv venv
        .\venv\Scripts\activate
        ```

4. Установка зависимостей

    Проект использует разные наборы зависимостей для продакшн-среды, тестирования и разработки. Зависимости разделены на три файла:

    - `requirements/prod.txt` — зависимости для продакшн-среды
    - `requirements/test.txt` — зависимости для тестирования
    - `requirements/dev.txt` — зависимости для разработки

    - **Установка продакшн-зависимостей**

        Для установки только продакшн-зависимостей, выполните следующую команду:

        ```bash
        pip install -r requirements/prod.txt
        ```

    - **Установка зависемостей для тестирования**

        Для установки только зависемостей для тестирования, выполните следующую команду:

        ```bash
        pip install -r requirements/test.txt
        ```  

    - **Установка зависемостей разработки**

        Для установки только зависемостей разработки, выполните следующую команду:

        ```bash
        pip install -r requirements/dev.txt
        ```  

5. Скопируйте файл `.env.template` в `.env`:

    - **Создание файла .env на основе шаблона .env.template** 

        ```bash
        cp .env.template .env
        ```

    ## Откройте файл .env и добавьте необходимые значения переменных окружения.

        DJANGO_SECRET_KEY="django-insecure-+9rpfah-dg7^9s0=w&p_bdy!yhfns^thwb0d@prthiqc91gs_@"
        DJANGO_DEBUG=True
        DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

6. Создайте суперпользователя для админ-панели:

    ```bash
    python3 manage.py createsuperuser
    ```
   
## Запуск проекта в dev-режиме

- **Для запуска тестов выполните следующую команду:**
    
    ```bash
    python3 manage.py test
    ```

- **Для запуска проекта в режиме разработки(developmentmode) выполните следующую команду:**

    ```bash
    python3 manage.py runserver
    ```
- **Для просмотора связей моделей проекта откройте файл ER-diagramma.jpg в корне проекта:**


