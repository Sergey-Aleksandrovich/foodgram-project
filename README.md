# Название проекта

foodgram-project - это проект, в котором возможно добавлять понравившиеся рецепты в покупки и получать список с необходимыми ингредиентами.

## Ссылка на пример проекта 

https://test-recipes.tk/?breakfast=True&lunch=True&dinner=True

## Быстрый старт

Эти инструкции позволят вам запустить копию проекта на вашем компьютере.

### Скачавание и запуск проекта

Скачайте данный проект на свой ПК

Установите необходимые настройки nginx, postgreSQL, django в файлах db.env, django.env, nginx.env.

Желательно получить сертификат SSL c помощью certbot.

Команда для запуска проекта
 
```
docker-compose up
```

### Команда для выполнения миграций

```
docker-compose exec web python manage.py migrate
```

### Заполнение базы начальными данными

Команда для заполнения базы начальными данными

```
docker-compose exec web python manage.py loaddata fixtures.json
```

### Команда для cбора статики

```
docker-compose exec web python manage.py collectstatic
```

### В фикстурах уже есть суперпользователь

Логин: admin

Пароль: 1231230
