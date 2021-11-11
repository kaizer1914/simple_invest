from base64 import b64decode
from io import StringIO

import pandas
from pandas import DataFrame

from moex_stock.bonds import BondsMarket
from moex_stock.shares import SharesMarket


class PositionReport:
    def __init__(self, file: str):
        self.file = file

    def get_from_file(self) -> DataFrame:
        content_type, content_string = self.file.split(',')
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

        position_df = DataFrame()
        for ticker in load_data['textBox14'].unique():  # Выделяем строки с уникальными тикерами
            series = load_data[load_data['textBox14'].isin([ticker])].tail(1)  # По указанному тикеру берём последнюю
            # строчку из датафрейма
            position_df = position_df.append(series, ignore_index=True)  # Добавляем строку в новый датафрейм

        # position_df.index = position_df['textBox14']  # Назначаем колонку с тикером в качествет идентификатора
        # position_df.index.name = 'ticker'  # Назначаем имя колонки идентификатора
        # position_df = position_df.drop(['textBox14'], axis='columns')  # Удаляем уже ненужную колонку с тикером

        ''' Переименовываем колонки '''
        position_df = position_df.rename(columns={'textBox1': 'position_name',
                                                  'textBox2': 'date',
                                                  'textBox11': 'buy_price',
                                                  'textBox22': 'count',
                                                  'textBox14': 'ticker',
                                                  'textBox8': 'commission'})
        return position_df

    def get_shares_report(self, columns: list = None) -> DataFrame:
        shares_market_df = SharesMarket.update_stock_data()
        '''Результат слияния датасета брокерского отчета с рынком акций биржи'''
        df = self.get_from_file().merge(shares_market_df, how='inner', left_on='ticker', right_on='ticker')
        df = df.rename(columns={'longname': 'name'})

        df['buy_sum'] = round(df['buy_price'] * df['count'], 2)
        df['current_sum'] = round(df['current_price'] * df['count'], 2)
        df['change_sum'] = round(df['current_sum'] - df['buy_sum'], 2)

        df['income'] = round((df['current_price'] - df['buy_price']) / df['buy_price'] * 100, 2)
        sum_shares = df.current_sum.sum(axis=0)
        df['weight'] = round(df['current_sum'] / sum_shares * 100, 2)

        if columns is None:
            return df
        else:
            return df[columns]

    def get_bonds_report(self, columns: list = None) -> DataFrame:
        bonds_market_df = BondsMarket.update_stock_data()
        '''Результат слияния датасета брокерского отчета с рынком облигаций биржи'''
        df = self.get_from_file().merge(bonds_market_df, how='inner', left_on='ticker', right_on='ticker')
        df = df.rename(columns={'longname': 'name'})

        df['current_price'] = round((df['price'] / 100 * df['nominal']) + df['nkd'], 2)
        df['current_sum'] = round(df['current_price'] * df['count'], 2)

        if columns is None:
            return df
        else:
            return df[columns]
