### FOODGRAM
![Foodgram workflow](https://github.com/troyanoff/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


## Описание

Сервис Foodgram - это агрегатор рецептов, в котором можно делиться соими рецептами с другими людьми или искать идеи для новых блюд. Здесь можно подписаться на любимых авторов, сформировать список самых любимых рецептов, а добавляя рецепты в корзину, можно скачать список тех ингредиентов, которые необходимо купить для своих кулинарных похождений. Также удобно фильтровать списки рецептов по тегам.


## Развертывание контейнера

> Предварительно у вас должны быть установлены Docker и Docker-compose

- Перейти в папку infra/;

- Создайте файл ".env" и поместите в него следущее:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

- Выполнить команду по развертыванию контейнера:

```sudo docker-compose up -d```

- Выполнить команду для сбора статики:

```sudo docker-compose exec web python manage.py collectstatic```

- Выполнить миграции:

```sudo docker-compose exec web python manage.py migrate```

- Создайте пользователя-админастратора:

```sudo docker-compose exec web python manage.py createsuperuser```

- Заполните базу данных популярными ингредиентами следующей командой:

```sudo docker-compose exec web python manage.py loadingr```

- Теперь проект доступен в вашем браузере по адресу localhost.


## Технологии:

- Python 3.9
- Django 4.1
- Django REST Framework 3.14
- Djoser
- Docker
- Docker-compose


## Над проектом трудились:

- Юрий Троянов
- Неизестный фронтэндер

## В контенер паковал:

- Юрий Троянов
