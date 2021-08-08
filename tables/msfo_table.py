import psycopg2

from tables.database_config import Database_config


class Msfo_table:
    __SECURITIES_TABLE = 'securities'
    __SHARES_TABLE = 'shares'

    def __init__(self, sec_id: str):
        self.__sec_id = sec_id
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"""
            CREATE TABLE IF NOT EXISTS {sec_id}
            (year SMALLINT PRIMARY KEY, 
            current_assets BIGINT,
            non_current_assets BIGINT,
            assets BIGINT,
            equity BIGINT,
            current_liabilities BIGINT,
            non_current_liabilities BIGINT,
            liabilities BIGINT,
            
            net_debt BIGINT,
            interest BIGINT,
            
            sales BIGINT,
            operating_income BIGINT,
            net_income BIGINT,
            
            ebitda BIGINT,
            fcf BIGINT,
            dividend BIGINT
            );
            """)
            connection.commit()

    def set_year(self, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"DELETE FROM {self.__sec_id} WHERE year = {year};")
            cursor.execute(F'INSERT INTO {self.__sec_id} VALUES ({year}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, '
                           F'{0}, {0}, {0}, {0}, {0}, {0});')
            connection.commit()

    def set_current_assets(self, current_assets: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET current_assets = {current_assets} WHERE year = {year};")
            connection.commit()

    def set_non_current_assets(self, non_current_assets: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET non_current_assets = {non_current_assets} "
                           F"WHERE year = {year};")
            connection.commit()

    def set_assets(self, assets: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET assets = {assets} WHERE year = {year};")
            connection.commit()

    def set_equity(self, equity: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET equity = {equity} WHERE year = {year};")
            connection.commit()

    def set_current_liabilities(self, current_liabilities: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET current_liabilities = {current_liabilities} "
                           F"WHERE year = {year};")
            connection.commit()

    def set_non_current_liabilities(self, non_current_liabilities: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET non_current_liabilities = {non_current_liabilities} "
                           F"WHERE year = {year};")
            connection.commit()

    def set_liabilities(self, liabilities: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET liabilities = {liabilities} WHERE year = {year};")
            connection.commit()

    def set_net_debt(self, net_debt: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET net_debt = {net_debt} WHERE year = {year};")
            connection.commit()

    def set_interest(self, interest: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET interest = {interest} WHERE year = {year};")
            connection.commit()

    def set_sales(self, sales: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET sales = {sales} WHERE year = {year};")
            connection.commit()

    def set_operating_income(self, operating_income: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET operating_income = {operating_income} "
                           F"WHERE year = {year};")
            connection.commit()

    def set_net_income(self, net_income: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET net_income = {net_income} WHERE year = {year};")
            connection.commit()

    def set_ebitda(self, ebitda: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET ebitda = {ebitda} WHERE year = {year};")
            connection.commit()

    def set_fcf(self, fcf: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET fcf = {fcf} WHERE year = {year};")
            connection.commit()

    def set_dividend(self, dividend: int, year: int):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"UPDATE {self.__sec_id} SET dividend = {dividend} WHERE year = {year};")
            connection.commit()

    def get_all_years(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT year FROM {self.__sec_id};")
            result = cursor.fetchall()
            years = list()
            for year in result:
                years.append(str(year[0]))
            years.sort()
            return years

    def get_count_years(self):
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT count(*) FROM {self.__sec_id};")
            return int(cursor.fetchone()[0])

    def get_current_assets(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT current_assets FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_non_current_assets(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT non_current_assets FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_assets(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT assets FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_equity(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT equity FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_current_liabilities(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT current_liabilities FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_non_current_liabilities(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT non_current_liabilities FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_liabilities(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT liabilities FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_net_debt(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT net_debt FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_interest(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT interest FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_sales(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT sales FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_operating_income(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT operating_income FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_net_income(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT net_income FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_ebitda(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT ebitda FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_fcf(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT fcf FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])

    def get_dividend(self, year: int) -> int:
        with psycopg2.connect(database=Database_config.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(F"SELECT dividend FROM {self.__sec_id} WHERE year = {year};")
            return int(cursor.fetchone()[0])
