#!/bin/bash

echo
echo "------------------------------------"
echo "Creating table ${MAIN_TABLE} in ${MYSQL_DATABASE} "
echo "------------------------------------"
echo
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "use ${MYSQL_DATABASE};" -e \
    "CREATE TABLE IF NOT EXISTS ${MAIN_TABLE}(
        id INT NOT NULL AUTO_INCREMENT,
        text TEXT,
        created_date DATETIME,
        rubrics  VARCHAR(100),
        PRIMARY KEY (id)
        );"

mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "SET GLOBAL local_infile=true;"

echo
echo "------------------------------------"
echo "Fill ${MAIN_TABLE} with posts.scv file"
echo "------------------------------------"
echo
mysql  -uroot -p${MYSQL_ROOT_PASSWORD}  ${MYSQL_DATABASE}  --local_infile=1 -e "use ${MYSQL_DATABASE};" -e \
     "LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/posts.csv'
      INTO TABLE ${MAIN_TABLE}
      FIELDS TERMINATED BY ','
      ENCLOSED BY '\"'
      LINES TERMINATED BY '\r\n'
      IGNORE 1 LINES (text, created_date, rubrics);"

