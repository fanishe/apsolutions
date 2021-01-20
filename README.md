# apsolutions
Необходимо написать очень простой поисковик по текстам документов. Данные хранятся в БД по желанию, поисковый индекс в эластике. 

Проект состоит из нескольких контейнеров:
1. Flask_mysql - База данных
  - Скачивается образ MySQL 8.0
  - При помощи переданного скрипта создается БД, наполняется содержимым из файла .csv

2. Adminer
  - Нужен для визуального просмотра БД
      > `http://localhost:8000`
      - Логин/пароль `admin`
      - Сервер - `database`
      - База данных - `main_base`

3. Flask_app
  - Основное web-приложение

## Запуск и тестирование
### Запуск
Предварительной настройки не требуется
- `docker-compose up --build`

### Тестирование
После того, как все контейнеры стартанули, тестирование проводится командой
-  `docker exec -it flask_app python3 runner.py`

## Основные методы и команды
Основной доступ к web-приложению осуществляется двумя способами:
- Web интерфейс
    - `http://localhost:8888/`
    - Поиск по содержимому в поле `text`
    - Вывод на экран (Немножко не очень красиво :)

- Командная строка
    - `/api_search` - принимает параметр `data=<sometext>`
        > `http://localhost:8888/api_search?data=hi`
      - Возвращает json ответ с ответом от БД
    - `/del` - принимает параметр `id=<num>`
        > `http://localhost:8888/del?id=1`
        - Возвращает json ответ от БД 
            - Если успешно:
              > `result:deleted`
            - Если нет:
              > `result:id_not_found`
    - Если данные не были переданы возвращает json ответ
        > {"result":"give_me_id"}
        > {"error" : "give_me_data"}

## Реализовано:
- [x] любой python фреймворк кроме Django и DRF;
- [x] `README` с гайдом по поднятию;
- [x] функциональные тесты;
- [x] сервис работает в Docker;
- [ ] `docs.json` - документация к сервису в формате openapi.
- [ ] асинхронные вызовы.
