CREATE TABLE IF NOT EXISTS main_table(
id INT NOT NULL AUTO_INCREMENT,
text TEXT,
created_date DATETIME,
rubrics  VARCHAR(100),
PRIMARY KEY (id)
);