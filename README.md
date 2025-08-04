# Мапа популярності локацій — Django + DRF

## Що реалізовано:

### 1. Аутентифікація:
- Реєстрація: `POST /api/register/`
- Логін: `POST /api/login/`
- Логаут: `POST /api/logout/`
- Скидання пароля через email: 
  - `/api/password-reset/`
  - `/api/password-reset-confirm/<uidb64>/<token>/` і тд 

### 2. Локації:
- Створення, оновлення, перегляд, видалення:
  - `GET /api/locations/` (підтримує фільтрацію + пошук)
  - `POST /api/locations/`
  - `GET/PUT/DELETE /api/locations/<id>/`
- Кешований список (без фільтра): `GET /api/cached-locations/`
- Вимкнути/увімкнути локацію: `POST /api/locations/<id>/toggle_active/`

### 3. Відгуки:
- Додати / переглянути: 
  - `GET /api/reviews/`
  - `POST /api/reviews/` (передати `location`, `text`, `rating`)
- Автоматично прив’язується до request.user

### 4. Лайки / дизлайки:
- `POST /api/reviews/<id>/like/`
- `POST /api/reviews/<id>/dislike/`
- `POST /api/review-likes/` — можна також напряму передавати review_id і is_like

### 5. Експорт:
- `GET /api/locations/export/?format=json` або `?format=csv`

### 6. Фільтрація / пошук:
- За назвою, описом (`search=...`)
- За категорією, середнім рейтингом (`?category=food&average_rating=4`)

### 7. Swagger-документація:
- `GET /swagger/` — автоматично згенерована документація всіх API
- Працює через бібліотеку `drf-yasg`, можна тестити прямо в браузері
- Не потрібен Postman

---

## Технології:
- Django, DRF, PostgreSQL
- Redis (кешування)
- DjangoFilter
- Pandas (експорт)
- drf-yasg (Swagger UI)

---

## Як запустити:
1. Redis: `docker run -d -p 6379:6379 redis` або `redis-server`
2. Міграції:
    ```
    poetry install
    poetry shell
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```
3. Запуск:
    ```
    python manage.py runserver
    ```

---

## Примітки:
- Усі ендпоінти префіксуються `/api/`
- Авторизація через cookie, працює сесія
- Swagger за адресою `/swagger/`
- Є базове кешування (`/cached-locations/`)
- Експорт працює на основі Pandas
