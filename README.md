## Установка и запуск проекта
1. Клонирование репозитория: 
   ```bash
   git clone git@github.com:voidCaloneian/django_bearer_jwt.git
   cd django_bearer_jwt
   ```
2. Запуск проекта
   ```bash
   docker compose up --build -d 
   ```
   **Подождите, пока контейнеры запустятся, прежде чем переходить к следующему шагу**
3. Создание и применение миграций
   ```bash
   docker compose exec web python src/manage.py makemigrations
   docker compose exec web python src.manage.py migrate
   ```
4. Опциональный запуск тестов
   ```bash
   docker compose exec web pytest
   ```

- **Сервис будет доступен по адресу:** ```http://localhost:8000``` (доступны любые локальные хосты, а также включены корс запросы с любого домена)
- Используйте ```TRADE.postman_collection.json``` для импорта готовой **Postman** коллекции

## API

- **POST** ```/api/accounts/signup/``` - регистрация пользователя
  
  **Параметры**
  
  ```identifier``` - ```string``` обязательный, **идентификатор** в формате почты, либо номера телефона (телефон начинающийся с 8 или +7 считается одинаковым)

  ```password``` - ```string``` обязательный, **пароль**
  
  **Пример**:
  
  ```json
  {
	"identifier": "void4function@gmail.com", 
    "password": "qwepassword123"
  }
  ```

  **Пример ответа**:
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```

- **POST** ```/api/accounts/signin/``` - авторизация пользователя
  
  **Параметры**
  
  ```identifier``` - ```string``` обязательный, **идентификатор** в формате почты, либо номера телефона (телефон начинающийся с 8 или +7 считается одинаковым)

  ```password``` - ```string``` обязательный, **пароль**
  
  **Пример**:
  ```json
  {
	"identifier": "void4function@gmail.com", 
    "password": "qwepassword123"
  }
  ```
  **Пример ответа**:
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```

- **POST** ```/api/accounts/logout/``` - логаут пользователя
- - Если ```all: true```, то удаляются все refresh токены
- - Если ```all: false```, то удаляется только указанный refresh токен
  
  **Заголовки**
  ```Authorization```: ```Bearer <access token>``` - ```JWT acess token``` обязательный 

  **Параметры**
  
  ```all``` - ```bool``` обязательный, **удалять ли все рефреш токены**

  ```refresh``` - ```string``` обязательный, **refresh token**, если ```all: false``` 
  
  **Пример**:
  
  ```Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxODU5MTAxLCJpYXQiOjE3NDE4NTg4MDEsImp0aSI6IjczMDE0YzFlZGYzYTQ5ZmQ4MmNkOTcxNGJhODg5ZDhkIiwidXNlcl9pZCI6MX0.FfxAiKsMlQIFys65qMJ_frSGELU01ynp4q5Pn4wPlYI```
  ```json
  {
	"all": false,
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTk0NTIwMSwiaWF0IjoxNzQxODU4ODAxLCJqdGkiOiI5NTIyOWNkOTI0NGU0ODc5OGIyMTA5OTZlNGEwODNkMyIsInVzZXJfaWQiOjF9.RldsMGrZR8GB8_TjM7BupRf2Pb6TWbHEyTwb-ur_x7I"
  }
  ```
  **Пример ответа**:
  
  ```json
  {
    "detail": "Текущий токен разлогинен",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxODU5MTIyLCJpYXQiOjE3NDE4NTg4MjIsImp0aSI6IjNhOTZmMGNkNjkzNDQzNzY4NTdkYjRhZTdiMGEwNjhiIiwidXNlcl9pZCI6MX0.7fMMYyqFDRvMQ4DUW8Bja1jvBB6wNrw7c7xYJl3opYI"
  }
  ```
- **GET** ```/api/accounts/info/``` - информация о пользователе
  
  **Заголовки**
  
  ```Authorization```: ```Bearer <access token>``` - ```JWT acess token``` обязательный

  **Пример**:
  
  ```Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxODU5MTAxLCJpYXQiOjE3NDE4NTg4MDEsImp0aSI6IjczMDE0YzFlZGYzYTQ5ZmQ4MmNkOTcxNGJhODg5ZDhkIiwidXNlcl9pZCI6MX0.FfxAiKsMlQIFys65qMJ_frSGELU01ynp4q5Pn4wPlYI```

  **Пример ответа**
  
  ```json
  {
    "identifier": "+79525295976",
    "id_type": "phone",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxODU5MzE4LCJpYXQiOjE3NDE4NTkwMTgsImp0aSI6IjViZDgxNzNhYWRkZjQ3NGU4NDc1NGNhZDkwMTY1ODE0IiwidXNlcl9pZCI6MX0.0r5hlrDsp6GLqENo_knI1R9JikyIM-RAnzVBDyRFUbw"
  }
  ```

- **GET** ```/api/accounts/info/``` - пинг до ya.ru
  
  **Заголовки**
  
  ```Authorization```: ```Bearer <access token>``` - ```JWT acess token``` обязательный 

  **Пример**:
  
  ```Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxODU5MTAxLCJpYXQiOjE3NDE4NTg4MDEsImp0aSI6IjczMDE0YzFlZGYzYTQ5ZmQ4MmNkOTcxNGJhODg5ZDhkIiwidXNlcl9pZCI6MX0.FfxAiKsMlQIFys65qMJ_frSGELU01ynp4q5Pn4wPlYI```

  **Пример ответа**
  
  ```json
  {
    "latency": 1.5751018524169922,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxODU3NzM1LCJpYXQiOjE3NDE4NTc0MzUsImp0aSI6IjBjMjI2MzM3YTFiNTQ4ZWY4NzlhMjU3NTIwZTkyZjQyIiwidXNlcl9pZCI6MX0.acQilqISTNaMESs0E2GlHLqgePg8xKTY-6u_BU1IMyA"
  }
  ```
