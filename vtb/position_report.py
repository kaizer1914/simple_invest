from base64 import b64decode
from io import StringIO

import pandas
from pandas import DataFrame
from sqlalchemy import create_engine

from moex_stock.bonds import BondsMarket
from moex_stock.shares_funds import SharesMarket


class PositionReport:
    def __init__(self):
        self.engine = create_engine('postgresql://kirill@localhost:5432/invest')
        self.table = 'position_report'

    def save_to_db(self, file: str):
        content_type, content_string = file.split(',')
        decoded_str = b64decode(content_string)
        load_data = pandas.read_csv(StringIO(decoded_str.decode('utf-8')))

        load_data = load_data[['textBox14', 'textBox1', 'textBox2', 'textBox7', 'textBox11', 'textBox22',
                               'textBox8']]  # Отбираем определенные столбцы
        load_data = load_data.fillna(0)  # Заменяем везде NaN на 0

        cash_index = load_data[load_data['textBox1'] == 0].index.values  # Определяем строки по иностранным валютам
        sell_index = load_data[load_data['textBox7'] != 0].index.values  # Определяем строки по проданным активам

        load_data = load_data.drop(index=cash_index)  # Удаляем строки по иностранным валютам
        load_data = load_data.drop(index=sell_index)  # Удаляем строки по проданным активам
        load_data = load_data.drop(['textBox7'], axis='columns')  # Удаляем столбец с датами закрытия позиций

        load_data[['textBox22']] = load_data[['textBox22']].replace(r'\s+', '',
                                                                    regex=True)  # Убираем пробелы в столбце count
        load_data[['textBox22']] = load_data[['textBox22']].astype(int)  # Назначаем тип данных

        result_data = DataFrame()
        for ticker in load_data['textBox14'].unique():  # Выделяем строки с уникальными тикерами
            series = load_data[load_data['textBox14'].isin([ticker])].tail(1)  # По указанному тикеру берём последнюю
            # строчку из датафрейма
            result_data = result_data.append(series, ignore_index=True)  # Добавляем строку в новый датафрейм

        result_data.index = result_data['textBox14']  # Назначаем колонку с тикером в качествет идентификатора
        result_data.index.name = 'ticker'  # Назначаем имя колонки идентификатора
        result_data = result_data.drop(['textBox14'], axis='columns')  # Удаляем уже ненужную колонку с тикером

        ''' Переименовываем колонки '''
        result_data = result_data.rename(columns={'textBox1': 'name',
                                                  'textBox2': 'date',
                                                  'textBox11': 'buy_price',
                                                  'textBox22': 'count',
                                                  'textBox8': 'commission'})
        result_data.to_sql(self.table, self.engine, if_exists='replace')

    def load_from_db(self) -> DataFrame:
        data = pandas.read_sql_table(self.table, self.engine)
        return data

    def merge_shares_data(self):
        shares_market_data = SharesMarket().update_stock_data()
        data = self.load_from_db()
        ''' Результат слияния датасета брокерского отчета с рынком акций биржи'''
        data = data.merge(shares_market_data, how='inner', left_on='ticker', right_on='ticker')
        return data

    def merge_bonds_data(self):
        bonds_market_data = BondsMarket().update_stock_data()
        data = self.load_from_db()
        data = data.merge(bonds_market_data, how='inner', left_on='ticker', right_on='ticker')
        return data

    def get_shares_data(self) -> DataFrame:
        data = self.merge_shares_data()
        data['income'] = (data['price'] - data['buy_price']) / data['buy_price']
        data['sum'] = data['price'] * data['count']
        '''Убираем лишние столбцы'''
        data = data[['longname', 'ticker', 'price', 'count', 'sum', 'income']]
        return data

    def get_bonds_data(self) -> DataFrame:
        data = self.merge_bonds_data()
        data['current_price'] = (data['price'] / 100 * data['nominal']) + data['nkd']
        '''Убираем лишние столбцы'''
        data = data[['longname', 'current_price', 'count', 'effectiveyield', 'couponperiod', 'duration',
                     'issuesize', 'enddate']]
        return data
