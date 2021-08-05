import psycopg2

from database_tables.database_config import Database_config


class Shares_table:
    __TABLE_NAME = 'shares'
    __SECURITIES_TABLE = 'securities'

    def __init__(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"""
            CREATE TABLE IF NOT EXISTS {self.__TABLE_NAME}
            (sec_id TEXT PRIMARY KEY, 
            sec_name TEXT,
            short_name TEXT,
            isin CHAR(12),
            price REAL,
            sec_type CHAR(1),
            list_level INT,
            lot_size INT,
            issue_size BIGINT
            );
            """)
            connection.commit()

    def add(self, sec_id, sec_name, short_name, isin, price, sec_type, list_level, lot_size, issue_size):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            # cursor.execute(F"select count(sec_id) from {self.__TABLE_NAME} where sec_id = \'{sec_id}\';")
            # exist = cursor.fetchall()
            # if exist[0][0] == 0:
            #     cursor.execute(F'INSERT INTO {self.__TABLE_NAME} VALUES (\'{sec_id}\', \'{sec_name}\', '
            #                    F'\'{short_name}\', \'{isin}\', {price}, \'{sec_type}\', {list_level}, {lot_value});')
            # else:
            #     cursor.execute(F'UPDATE {self.__TABLE_NAME} SET sec_name = \'{sec_name}\', '
            #                    F'short_name = \'{short_name}\', isin = \'{isin}\', price = {price}, '
            #                    F'sec_type = \'{sec_type}\', list_level = {list_level}, lot_value = {lot_value} '
            #                    F'WHERE sec_id = \'{sec_id}\';')
            cursor.execute(F"DELETE FROM {self.__TABLE_NAME} WHERE sec_id = \'{sec_id}\';")
            cursor.execute(F'INSERT INTO {self.__TABLE_NAME} VALUES (\'{sec_id}\', \'{sec_name}\', '
                           F'\'{short_name}\', \'{isin}\', {price}, \'{sec_type}\', {list_level}, {lot_size}, {issue_size});')
            connection.commit()

    def remove(self, sec_id):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"DELETE FROM {self.__TABLE_NAME} WHERE sec_id = \'{sec_id}\';")
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

    def clear_table(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F'DELETE FROM {self.__TABLE_NAME};')
            connection.commit()

    def get_total_cost(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT sum (price * count) FROM {self.__TABLE_NAME}, {self.__SECURITIES_TABLE} WHERE "
                           F"{self.__TABLE_NAME}.sec_id = {self.__SECURITIES_TABLE}.sec_id;")
            return cursor.fetchall()[0][0]

    def get_sec_and_cost(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            shares_cost = dict()
            cursor = connection.cursor()
            cursor.execute(F"SELECT {self.__TABLE_NAME}.sec_id, price * count "
                           F"FROM {self.__TABLE_NAME}, {self.__SECURITIES_TABLE} WHERE "
                           F"{self.__TABLE_NAME}.sec_id = {self.__SECURITIES_TABLE}.sec_id;")
            for row in cursor.fetchall():
                shares_cost[row[0]] = row[1]
            return shares_cost
