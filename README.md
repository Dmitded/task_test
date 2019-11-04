# Test task LTP
Приложение для автоматизации и контроля сбора урожая

### Конфигурация nginx

```nginx
map $http_upgrade $connection_upgrade {
  default upgrade;
  ‘’ close;
}

upstream frontend {
  server 127.0.0.1:8080;
}

upstream backend {
  server 127.0.0.1:8000;
}

server {
  listen 80;
  server_name moon.local;
  client_max_body_size 100M;

  location /api {
    proxy_pass http://backend/;
    proxy_set_header Host 127.0.0.1;
  }

  location / {
    proxy_pass http://frontend/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection “upgrade”;
    proxy_set_header Host 127.0.0.1;
  }
}
```
Для запуска приложения необходимо установить необходимые пакеты

(apt-get install (Ubuntu) / brew install (Mac OS)):

python3, redis, postgresql, npm, nodejs

### backend

В папке backend в файле config.py необходимо изменить поля username и password на свои имя пользователя и пароль в postgres

```bash
psql postgres
create database tasktest;
\q
```

```bash
cd backend
python3 -m venv env
./env/bin/pip3 install -r requirements.txt
./env/bin/alembic upgrade head # запуск миграций
chmod +x test_data.py
./test_data.py # заполнение БД тестовыми значениями и запись данных для входа в файл inspector.txt
./dev.sh # запуск (gunicorn)
```

### frontend
cd frontend

## Установка проекта
```
npm install
```

### Компиляция и hot-reload для разработки
```
npm run serve
```

### Сборка под продакшн
```
npm run build
```

### Описание Front-End
После запуска появляется страница логина:
  В поле Login нужно указать id Инспектора, в тестовой DB
  это был 25 id;
  В поле Пароля нужно указать пароль Инспектора, в тестовой DB
  генерировался файл с Паролем по директории /backend/inspector.txt.

После входа перед нами появляется:
  На десктопной версии сайта:
    В верхней части находится toolbar с поиском по значениям в таблице, выбор даты,
    для обновления таблицы и графика, и обновление данных (возвращает сегодняшний день),
    logout для выхода из панели;
    С левой стороны таблица, в которой отображается лог действий рабочего;
    С правой стороны выводится график (цвета графика генерируются динамически)
  На мобильной версии сайта:
    В верхней части находится toolbar с выбором даты,
    для обновления таблицы и графика, и обновление данных (возвращает сегодняшний день),
    logout для выхода из панели;
    В верхней части отображается график;
    Ниже Поиск по таблице и сама таблица.
```
```

### Описание API
[POST] /api/login  ` Авторизация пользователя `

```json
{
  "ean13": 25,
  "password": "password"
}
```

[GET] /api  ` Check API version `

[GET] /api/users/current  ` Получение данных об авторизованном пользователе `

[GET] /api/activity?day=2019-05-13  ` Получение сведений об активности за дату - 2019-05-13 `

## Пояснения к выполненной работе

На основе исходных файлов было сделано предположение, приложение будут использовать 2 типа пользователей - сборщик и инспектор.
В приложении происходит запись данных о собранном урожае пользователем - Инспектор.
На основе записанных данных строится таблица активности сборщиков.

Для пользователей была сделана авторизация.
Возможность получить данные есть только у инспектора.
Неиспользуемые зависимости в файлах были закомментированы или удалены.


