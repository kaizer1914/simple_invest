import psycopg2

from database_tables.database_config import Database_config


class Bonds_table:
    __TABLE_NAME = 'bonds'
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
            sec_type CHAR(1), 
            list_level INT, 
            price NUMERIC(5,2), 
            lot_value INT, 
            nkd NUMERIC(5,2), 
            coupon_value NUMERIC(5,2), 
            coupon_period INT, 
            coupon_percent NUMERIC(5,2), 
            next_coupon DATE, 
            mat_date DATE, 
            offer_date DATE, 
            yield_date_type TEXT, 
            effective_yield NUMERIC(5,2), 
            yield_date DATE, 
            duration INT
            );
            """)
            connection.commit()

    def add(self, sec_id, sec_name, short_name, isin, sec_type, list_level, price, lot_value, nkd, coupon_value,
            coupon_period, coupon_percent, next_coupon, mat_date, offer_date, yield_date_type, effective_yield,
            yield_date, duration):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"DELETE FROM {self.__TABLE_NAME} WHERE sec_id = \'{sec_id}\';")
            cursor.execute(F"INSERT INTO {self.__TABLE_NAME} VALUES (\'{sec_id}\', \'{sec_name}\', \'{short_name}\', "
                           F"\'{isin}\', \'{sec_type}\', {list_level}, {price}, {lot_value}, {nkd}, {coupon_value}, "
                           F"{coupon_period}, {coupon_percent}, \'{next_coupon}\', \'{mat_date}\', \'{offer_date}\', "
                           F"\'{yield_date_type}\', {effective_yield}, \'{yield_date}\', {duration});"
                           )
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

    def get_ofz_cost(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT sum((price / 100 * lot_value + nkd) * count) "
                           F"FROM {self.__TABLE_NAME}, {self.__SECURITIES_TABLE} WHERE "
                           F"{self.__TABLE_NAME}.sec_id = {self.__SECURITIES_TABLE}.sec_id AND sec_type = '3';")
            return cursor.fetchall()[0][0]

    def get_corporate_cost(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT sum((price / 100 * lot_value + nkd) * count) "
                           F"FROM {self.__TABLE_NAME}, {self.__SECURITIES_TABLE} WHERE "
                           F"{self.__TABLE_NAME}.sec_id = {self.__SECURITIES_TABLE}.sec_id AND (sec_type = '6' OR "
                           F"sec_type = '7' OR sec_type = '8');")
            return cursor.fetchall()[0][0]

    def get_region_cost(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT SUM((price / 100 * lot_value + nkd) * count) "
                           F"FROM {self.__TABLE_NAME}, {self.__SECURITIES_TABLE} WHERE "
                           F"{self.__TABLE_NAME}.sec_id = {self.__SECURITIES_TABLE}.sec_id AND (sec_type = '4' OR "
                           F"sec_type = '5' OR sec_type = 'C');")
            return cursor.fetchall()[0][0]

    def get_total_cost(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT sum((price / 100 * lot_value + nkd) * count) "
                           F"FROM {self.__TABLE_NAME}, {self.__SECURITIES_TABLE} WHERE "
                           F"{self.__TABLE_NAME}.sec_id = {self.__SECURITIES_TABLE}.sec_id;")
            return cursor.fetchall()[0][0]
