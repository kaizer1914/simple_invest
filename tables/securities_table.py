import psycopg2

from tables.database_config import Database_config


class Securities_table:
    __TABLE_NAME = 'securities'
    __ETF_TABLE = 'etf'
    __SHARES_TABLE = 'shares'
    __BONDS_TABLE = 'bonds'

    def __init__(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"""
            CREATE TABLE IF NOT EXISTS {self.__TABLE_NAME}
            (sec_id TEXT PRIMARY KEY, 
            count INT, 
            buy_price REAL
            );
            """)
            connection.commit()

    def add(self, sec_id, count, buy_price):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"DELETE FROM {self.__TABLE_NAME} WHERE sec_id = \'{sec_id}\';")
            cursor.execute(F'INSERT INTO {self.__TABLE_NAME} VALUES (\'{sec_id}\', {count}, {buy_price});')
            connection.commit()

    def remove(self, sec_id):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F'DELETE FROM {self.__TABLE_NAME} WHERE sec_id = ?', (sec_id,))
            connection.commit()

    def get_all(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F'SELECT * FROM {self.__TABLE_NAME};')
            return cursor.fetchall()

    def get_sec_id(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F'SELECT sec_id FROM {self.__TABLE_NAME};')
            result = cursor.fetchall()
            sec_id = list()
            for sec in result:
                sec_id.append(sec[0])
            return sec_id

    def get_count(self, sec_id):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F'SELECT count FROM {self.__TABLE_NAME} WHERE sec_id = ?;', (sec_id,))
            count = cursor.fetchone()[0]
            return count

    def clear_table(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F'DELETE FROM {self.__TABLE_NAME};')
            connection.commit()
