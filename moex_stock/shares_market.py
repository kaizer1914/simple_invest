import pandas
from pandas import DataFrame
from sqlalchemy import create_engine


# https://iss.moex.com/iss/engines/stock/markets/shares/securities.xml?iss.meta=off - список всех акций
# https://iss.moex.com/iss/engines/stock/markets/shares.xml?iss.meta=off  - справка по рынкам акций

class SharesMarket:
    def __init__(self):
        self.engine = create_engine('postgresql://kirill@localhost/invest')
        self.table = 'shares_market'

    def update_stock_data(self) -> DataFrame:
        url = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities.json?iss.meta=off'

        response_data = pandas.read_json(url)
        securities = response_data['securities']
        market = response_data['marketdata']

        '''Задаем содержимое и заголовки колонок'''
        securities_data = DataFrame(data=securities.data, columns=securities.columns)
        market_data = DataFrame(data=market.data, columns=market.columns)

        securities_data = securities_data.merge(market_data, how='left')  # Объединяем таблицы
        securities_data = securities_data.fillna(0)  # Замена NaN на 0

        '''Ищем и удаляем строки'''
        small_index = securities_data[securities_data['BOARDID'] == 'SMAL'].index.values  # Неполные лоты (акции)
        speq_index = securities_data[securities_data['BOARDID'] == 'SPEQ'].index.values  # Поставка по СК (акции)
        tqdp_index = securities_data[securities_data['BOARDID'] == 'TQDP'].index.values  # Крупные пакеты - Акции

        securities_data = securities_data.drop(index=small_index)
        securities_data = securities_data.drop(index=speq_index)
        securities_data = securities_data.drop(index=tqdp_index)

        null_price_index = securities_data[securities_data['LAST'] == 0].index.values
        securities_data = securities_data.drop(index=null_price_index)

        '''Отбираем нужные колонки'''
        securities_data = securities_data[
            ['SECID', 'SHORTNAME', 'SECNAME', 'ISIN', 'LAST', 'DECIMALS', 'LOTSIZE', 'CURRENCYID',
             'ISSUECAPITALIZATION', 'SECTYPE', 'LISTLEVEL']]

        '''Назначаем тикер в качестве индекса'''
        securities_data.index = securities_data['SECID']
        securities_data.index.name = 'ticker'
        securities_data = securities_data.drop(['SECID'], axis=1)

        '''Переименовываем колонки'''
        securities_data = securities_data.rename(columns={'SHORTNAME': 'shortname',
                                                          'SECNAME': 'longname',
                                                          'ISIN': 'isin',
                                                          'LAST': 'price',
                                                          'DECIMALS': 'decimals',
                                                          'LOTSIZE': 'lotsize',
                                                          'CURRENCYID': 'currency',
                                                          'ISSUECAPITALIZATION': 'market_cap',
                                                          'SECTYPE': 'sectype',
                                                          'LISTLEVEL': 'listlevel'
                                                          })
        securities_data.to_sql(self.table, self.engine, if_exists='replace')  # Сохраняем в БД
        return securities_data

    def get_stock_data(self) -> DataFrame:
        data = pandas.read_sql_table(self.table, self.engine)
        return data


if __name__ == '__main__':
    shares = SharesMarket()
    shares.update_stock_data()
