#!/bin/bash

mysql -uroot -proot -e "SET GLOBAL local_infile=true;"

mysql  -uroot -proot  main_base  --local_infile=1 -e "use main_base;" -e \
     "LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/posts.csv'
      INTO TABLE main_table
      FIELDS TERMINATED BY ','
      ENCLOSED BY '\"'
      LINES TERMINATED BY '\r'
      IGNORE 1 LINES (text, created_date, rubrics);"

