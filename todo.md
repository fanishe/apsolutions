# TODO

## Создать БД
1. [v] Построить контйнер с БД
2. [v] Создать таблицу с помощью `.sql` файла
3. [v] При запуске контейнера, наполняется БД

Подключится к БД для ручной проверки
`docker exec -it mysql_global mysql -uroot -proot`
### Insert csv to db
```sql
set global local_infile=true

LOAD DATA LOCAL INFILE '/mydata/posts.csv' 
  INTO TABLE main_table 
  FIELDS TERMINATED BY ',' 
  ENCLOSED BY '"' 
  LINES TERMINATED BY '\n' 
  IGNORE 1 LINES (text, created_date, rubrics)"'
```

## Обработчик

