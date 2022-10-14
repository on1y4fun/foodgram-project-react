Для ревью:
Адрес сервиса http://178.154.224.147/
Суперюзер
логин:
    qwerty@qwerty.com
пароль:
    admin


# Проект Foodgram

Сайт Foodgram — база рецептов.

## Описание проекта

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/on1y4fun/foodgram-project-react.git

```
Запуск приложения в контейнерах:

```
cd infra/
```
```
docker-compose up -d --build
```

Выполняем миграции:

```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```
Собираем статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```
Команда на заполнение базы данных ингредиентами:

```
docker-compose exec web python manage.py ingredients_to_postgres
```

## Автор бэкенд части

[Максим Чен](https://github.com/on1y4fun)

### Лицензия [MIT](https://opensource.org/licenses/MIT)