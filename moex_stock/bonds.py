import pandas
from pandas import DataFrame
from sqlalchemy import create_engine


# https://iss.moex.com/iss/engines/stock/markets/bonds/securities.xml?iss.meta=off - список всех облигаций
# https://iss.moex.com/iss/engines/stock/markets/bonds.xml?iss.meta=off  - справка по рынкам облигаций
class BondsMarket:
    def __init__(self):
        self.engine = create_engine('postgresql://kirill@localhost/invest')
        self.table = 'bonds_market'

    def update_stock_data(self) -> DataFrame:
        url = 'https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?iss.meta=off'

        response_data = pandas.read_json(url)
        securities = response_data['securities']
        market_yields = response_data['marketdata_yields']

        '''Задаем содержимое и заголовки колонок'''
        securities_data = DataFrame(data=securities.data, columns=securities.columns)
        market_yields_data = DataFrame(data=market_yields.data, columns=market_yields.columns)

        securities_data = securities_data.merge(market_yields_data, how='left')  # Объединяем таблицы
        securities_data = securities_data.fillna(0)  # Замена NaN на 0

        empty_index = securities_data[securities_data['PRICE'] == 0].index.values  # Ищем строки с нулевой ценой

        '''Удаляем такие строки'''
        securities_data = securities_data.drop(index=empty_index)

        '''Отбираем нужные колонки'''
        securities_data = securities_data[
            ['SECID', 'SHORTNAME', 'SECNAME', 'ISIN', 'PRICE', 'DECIMALS', 'ACCRUEDINT', 'LOTVALUE',
             'LOTSIZE', 'CURRENCYID', 'COUPONVALUE', 'COUPONPERCENT', 'COUPONPERIOD', 'NEXTCOUPON', 'EFFECTIVEYIELD',
             'DURATION', 'YIELDDATE', 'YIELDDATETYPE', 'OFFERDATE', 'MATDATE', 'ISSUESIZEPLACED', 'SECTYPE',
             'LISTLEVEL']]

        '''Назначаем тикер в качестве индекса'''
        securities_data.index = securities_data['SECID']
        securities_data.index.name = 'ticker'
        securities_data = securities_data.drop(['SECID'], axis=1)

        '''Переименовываем колонки'''
        securities_data = securities_data.rename(columns={'SHORTNAME': 'shortname',
                                                          'SECNAME': 'longname',
                                                          'ISIN': 'isin',
                                                          'PRICE': 'price',
                                                          'DECIMALS': 'decimals',
                                                          'ACCRUEDINT': 'nkd',
                                                          'LOTVALUE': 'nominal',
                                                          'LOTSIZE': 'lotsize',
                                                          'CURRENCYID': 'currency',
                                                          'COUPONVALUE': 'couponvalue',
                                                          'COUPONPERCENT': 'couponpercent',
                                                          'COUPONPERIOD': 'couponperiod',
                                                          'NEXTCOUPON': 'nextcoupon',
                                                          'EFFECTIVEYIELD': 'effectiveyield',
                                                          'DURATION': 'duration',
                                                          'YIELDDATE': 'yielddate',
                                                          'YIELDDATETYPE': 'endtype',
                                                          'OFFERDATE': 'offerdate',
                                                          'MATDATE': 'enddate',
                                                          'ISSUESIZEPLACED': 'issuesize',
                                                          'SECTYPE': 'sectype',
                                                          'LISTLEVEL': 'listlevel'
                                                          })

        securities_data.to_sql(self.table, self.engine, if_exists='replace')  # Сохраняем в БД
        return securities_data

    def get_stock_data(self) -> DataFrame:
        data = pandas.read_sql_table(self.table, self.engine)
        return data
