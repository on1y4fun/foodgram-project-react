# Проект Foodgram

Сайт Foodgram — база рецептов.

## Описание проекта

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/on1y4fun/foodgram-project-react.git

```
### Запуск бэкенда:

```
cd backend/
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd foodgram/
```
```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Запуск фронтенда:

```
cd frontend/
```

Установить зависимости:

```
npm i 
```

Запустить проект:

```
npm run start 
```

## Автор бэкенд части

[Максим Чен](https://github.com/on1y4fun) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них.

### Лицензия [MIT](https://opensource.org/licenses/MIT)