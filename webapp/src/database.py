from configparser import ConfigParser
import logging
import json
import time
import mysql.connector
import mysql.connector.pooling


class Database():
    """class for database"""
    def __init__(self, config_file, section, table):
        self.config_file = config_file
        self.section = section
        self.table = table
        self.db_config = self.read_dbconfig()
        self.connect()

    def connect(self):
        while True:
            try:
                self.conn_pool = (
                    mysql.connector.pooling.MySQLConnectionPool(
                        pool_size=10, **self.db_config))

            except mysql.connector.errors.InterfaceError as exc:
                logging.error(exc)
                time.sleep(3)
            else:
                logging.info("Connected to DataBase")
                break

    def get_conn(self):
        while True:
            try:
                conn = self.conn_pool.get_connection()
                conn.autocommit = True
            except Exception as err:
                logging.exception(err)
                time.sleep(1)
            else:
                return conn

    def read_dbconfig(self):
        """Читаем конфиг файл с инфой о БД"""
        if self.config_file.endswith('.ini'):
            parser = ConfigParser()
            parser.read(self.config_file)

            dbase = {}
            if parser.has_section(self.section):
                items = parser.items(self.section)
                for item in items:
                    dbase[item[0]] = item[1]
            else:
                raise Exception(
                    "Section '{}' not found in the file '{}'".format(
                        self.section, self.config_file))
            return dbase

        if self.config_file.endswith('.json'):
            with open(self.config_file, 'r') as file:
                parser = json.load(file)
            dbase = {}

            items = parser[self.section]
            for item in items:
                dbase[item] = items[item]
            return dbase

    def _run_query(self, query_command):
        """Основной метод выполняющий запосы в БД
            Он нужен, чтобы не делать громоздкие методы
        """
        while True:
            cursor = None
            logging.info("Run Query %s", query_command)
            try:
                datas = []
                conn = self.get_conn()
                cursor = conn.cursor()
                cursor.execute(query_command)
                for row in cursor:
                    datas.append(row)
                conn.commit()

            except mysql.connector.errors.OperationalError as err:
                logging.error(err)
                self.connect()
            except mysql.connector.errors.InterfaceError as err:
                logging.exception(err)
                self.connect()
            except Exception as err:
                logging.exception(err)
            else:
                logging.info("Result of Query - %s", datas)
                return datas
            finally:
                conn.close()
                if cursor:
                    cursor.close()

    def search_text(self, text):
        data = self._run_query(
            f"""SELECT
                    *
                FROM {self.table}
                WHERE
                     text  LIKE '%{text}%'
                ORDER BY created_date
                LIMIT 20;
            """)
        return data

    def delete_row(self, row_id):
        """ Delete row from table """
        data = self._run_query(
            f"""SELECT id
                FROM {self.table}
                WHERE id = {row_id}
            """)
        if data:
            self._run_query(
                f"""DELETE
                    FROM {self.table}
                    WHERE id = {row_id}
                """)
            exit_code = 0
        else:
            exit_code = 1

        return exit_code
