# CityEvents

Городская афиша событий: мероприятия, площадки, организаторы, билеты, избранное и отзывы.

Домен: `cityevents.isgood.host`

## Установка

1. Создайте виртуальное окружение и активируйте его.
2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `.env.example`.
4. Выполните миграции:

```bash
python manage.py migrate
```

5. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

6. Заполните тестовые данные:

```bash
python manage.py seed
```

7. Запустите локально:

```bash
python manage.py runserver
```

## Тестовые логины

- Администратор: создайте через `createsuperuser`.
- demo_user / DemoPass123
- demo_org / DemoPass123

## Шаблон дизайна

Использован бесплатный шаблон **JobBoard2 (Template 606)** с сайта freehtmlthemes.ru.
Источник: `https://freehtmlthemes.ru/categories/business/template-606`
Файлы шаблона находятся в `static/vendor/template-606/`.

## Архитектура

- 10+ приложений Django (events, venues, organizers, orders, tickets, users и др.)
- 15+ моделей, связи FK/M2M
- Единый базовый шаблон `templates/base.html`
- Кастомные страницы ошибок `404.html`, `500.html`
- Рейтинги и средний рейтинг событий (отзывы 1–5)
- Роли: user / organizer / staff (группы и permissions создаются в `seed`)
- Регистрация требует подтверждения email (в DEBUG письмо выводится в консоль).

## API

Примеры эндпоинтов:

- `GET /api/events/` — список событий (пагинация + фильтры q, category, city, ordering, year)
- `GET /api/events/<slug>/` — детальная информация
- `POST /api/events/` — создать (только авторизованные)
- `PUT /api/events/<slug>/` — обновить (только авторизованные)
- `DELETE /api/events/<slug>/` — удалить (только авторизованные)
- `GET /api/categories/` — список категорий
- `GET /api/venues/` — список площадок
- `GET /api/reviews/?event=<slug>` — отзывы

Примеры:

```http
GET /api/events/?q=концерт&city=almaty&ordering=start_at&page=1&page_size=5
```

```json
{
  "count": 12,
  "page": 1,
  "pages": 3,
  "results": [
    {
      "id": 1,
      "title": "Городской концерт",
      "slug": "city-concert",
      "start_at": "2026-02-21T12:00:00+06:00",
      "end_at": "2026-02-21T14:00:00+06:00",
      "venue": "City Hall",
      "organizer": "CityEvents Team",
      "categories": ["Музыка"],
      "tags": ["Бесплатно"],
      "price_from": "0.00",
      "status": "published",
      "avg_rating": 4.8,
      "reviews_count": 10
    }
  ]
}
```

```http
POST /api/events/
Content-Type: application/json
```

```json
{
  "title": "Jazz Night",
  "start_at": "2026-03-01T19:00:00+06:00",
  "end_at": "2026-03-01T21:00:00+06:00",
  "venue_id": 1,
  "organizer_id": 1,
  "price_from": 2000,
  "status": "draft"
}
```

```json
{
  "id": 2,
  "title": "Jazz Night",
  "slug": "jazz-night",
  "start_at": "2026-03-01T19:00:00+06:00",
  "end_at": "2026-03-01T21:00:00+06:00",
  "venue": "City Hall",
  "organizer": "CityEvents Team",
  "categories": [],
  "tags": [],
  "price_from": "2000.00",
  "status": "draft",
  "avg_rating": null,
  "reviews_count": 0
}
```

## Деплой и эксплуатация

- `DEBUG=False` на проде
- `collectstatic` на сервере:

```bash
python manage.py collectstatic
```


- PostgreSQL на проде (параметры в `.env`: POSTGRES_DB/USER/PASSWORD/HOST/PORT)
- HTTPS включён через Certbot, автообновление сертификата по таймеру `certbot.timer`
- Логи: используйте вывод в консоль веб-сервера (systemd/journalctl или панель хостинга)
- Перезапуск: через панель хостинга или systemd (если используется)
- Резервные копии: регулярный дамп PostgreSQL (`pg_dump`) и хранение архивов

## SMTP

Парольный reset работает через SMTP. Укажите настройки в `.env` (EMAIL_HOST/USER/PASSWORD).
Если SMTP не настроен, можно оставить эту функцию как заглушку — опишите это в README и не демонстрируйте на проде.

## Языки

Переключатель языков включён (RU/EN). Для реальных переводов:

```bash
python manage.py makemessages -l en
python manage.py compilemessages
```

Файлы переводов размещаются в `locale/`.

## Сервис

Управление сервисом (Gunicorn):

```bash
systemctl status cityevents --no-pager
systemctl restart cityevents
```

Nginx:

```bash
nginx -t
systemctl reload nginx
```

## Безопасность

- Ограничение частоты логина: 5 неудачных попыток за 10 минут блокируют вход.

## Дополнительно

- Избранное для пользователя.
- Отзывы/рейтинги 1–5 и средний рейтинг события.
- Живой фильтр списка событий на JS.
- Темная/светлая тема с сохранением в localStorage.
