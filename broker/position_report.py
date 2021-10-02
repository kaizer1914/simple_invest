import pandas
from pandas import DataFrame
from sqlalchemy import create_engine


class PositionReport:
    def __init__(self):
        self.engine = create_engine('postgresql://kirill@localhost:5432/invest')
        self.table = 'position_report'

    def save_to_db(self, file: str):
        load_data = pandas.read_csv(file)
        load_data = load_data[['textBox14', 'textBox1', 'textBox2', 'textBox7', 'textBox11', 'textBox22',
                               'textBox8']]  # Отбираем определенные столбцы
        load_data = load_data.fillna(0)  # Заменяем везде NaN на 0

        cash_index = load_data[load_data['textBox1'] == 0].index.values  # Определяем строки по иностранным валютам
        sell_index = load_data[load_data['textBox7'] != 0].index.values  # Определяем строки по проданным активам

        load_data = load_data.drop(index=cash_index)  # Удаляем строки по иностранным валютам
        load_data = load_data.drop(index=sell_index)  # Удаляем строки по проданным активам
        load_data = load_data.drop(['textBox7'], axis='columns')  # Удаляем столбец с датами закрытия позиций

        result_data = DataFrame()
        for ticker in load_data['textBox14'].unique():  # Выделяем строки с уникальными тикерами
            series = load_data[
                load_data['textBox14'].isin(
                    [ticker])].max()  # Оставляем строки с максимальным индексом по каждому тикеру
            result_data = result_data.append(series, ignore_index=True)

        result_data.index = result_data['textBox14']  # Назначаем колонку с тикером в качествет идентификатора
        result_data.index.name = 'ticker'  # Назначаем имя колонки идентификатора
        result_data = result_data.drop(['textBox14'], axis='columns')  # Удаляем уже ненужную колонку с тикером

        ''' Переименовываем колонки '''
        result_data = result_data.rename(columns={'textBox1': 'name',
                                                  'textBox2': 'data',
                                                  'textBox11': 'price',
                                                  'textBox22': 'count',
                                                  'textBox8': 'commission'})

        result_data[['count']] = result_data[['count']].replace(r'\s+', '',
                                                                regex=True)  # Убираем пробелы в столбце count
        result_data[['count']] = result_data[['count']].astype(int)  # Назначаем тип данных
        result_data.to_sql(self.table, self.engine, if_exists='replace')

    def load_from_db(self) -> DataFrame:
        data = pandas.read_sql_table(self.table, self.engine)
        return data
