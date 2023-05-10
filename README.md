# Решение тестового задания

## Оглавление
1. [Оглавление](##Оглавление)
2. [Требования](##Требования)
3. [Запуск](##Запуск)
4. [Примеры](##Примеры)

## Требования
ЯП: Python 3.11, БД: SQLite

## Запуск
1. Создать виртуальное окружение
2. pip install -r requirements.txt
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py runserver

## Примеры
### 1. /api/create_user
METHOD POST, создание пользователя по никнейму и возврат его id

Пример

Request \
POST: /api/create_user \
JSON: {"username": "andrey"}

Response \
CODE: 200 \
1

### 2. /api/user/int:from_user/invite/int:to_user
METHOD POST, создание заявки на добавление в друзья пользователем from_user
для to_user \
Возможны различные ответы и реакции на запрос в друзья, например, 
если пользователь1 отправляет заявку в друзья пользователю2, а
пользователь2 отправляет заявку пользователю1, то они автоматом становятся 
друзьями, их заявки автоматом принимаются



Пример

Request \
POST: /api/user/1/invite/2 

Response \
CODE: 200 \
"Заявка успешно отправлена"

### 3. /api/user/int:to_user/accept/int:from_user
METHOD POST, принятие заявки, т.е. создание пары друзей

Пример

Request \
POST: /api/user/2/accept/1 

Response \
CODE: 200 \
"Заявка принята"

### 4. /api/user/int:to_user/decline/int:from_user
METHOD POST, отклонение заявки в друзья

Пример

Request \
POST: /api/user/1/decline/7 

Response \
CODE: 400 \
"Заявка не найдена"

### 5. /api/user/int:user/invites
METHOD POST, увидеть все приглашения в друзья

Пример

Request \
POST: /api/user/1/invites

Response \
CODE: 200 \
JSON: [
    {
        "from_user": 4
    }, 
    {
        "from_user": 5
    }
]

### 6. /api/user/int:user/sent_invites
METHOD POST, увидеть все отправленные приглашения

Пример

Request \
POST: /api/user/1/sent_invites

Response \
CODE: 200 \
JSON: [
    {
        "to_user": 34
    }, 
    {
        "to_user": 555
    }
]

### 7. /api/user/int:user/friends
METHOD POST, увидеть всех друзей

Пример

Request \
POST: /api/user/1/friends

Response \
CODE: 200 \
JSON: 
[
    {
        "user1": 9,
        "user2": 1
    },
    {
        "user1": 9,
        "user2": 2
    },
    {
        "user1": 9,
        "user2": 3
    },
    {
        "user1": 9,
        "user2": 6
    },
    {
        "user1": 7,
        "user2": 9
    }
]

### 8. /api/user/int:from_user/status/int:to_user
METHOD POST, увидеть статус между двумя пользователями

Пример

Request \
POST: /api/user/1/status/5

Response \
CODE: 200 \
"Нет статуса"

### 9. /api/user/int:from_user/delete_friend/int:to_user
METHOD POST, разорвать дружбу между двумя пользователями

Пример

Request \
POST: /api/user/1/delete_friend/10

Response \
CODE: 200 \
"Больше не друзья"