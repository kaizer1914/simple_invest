import json

import requests

from moex_stock_data.check_security import Check_security


class Moex_stock_data:
    # TQTF - Т+: ETF - безадрес.
    # TQBR - Т+: Акции и ДР - безадрес.
    # TQCB - Т+: Облигации - безадрес.
    # TQOB - Т+: Гособлигации - безадрес.

    # https://iss.moex.com/iss/engines/stock/markets/shares/securities.xml?iss.meta=off - список всех акций
    # https://iss.moex.com/iss/engines/stock/markets/bonds/securities.xml?iss.meta=off - список всех облигаций
    # https://iss.moex.com/iss/engines/stock/markets/shares.xml?iss.meta=off  - справка по рынкам акций
    # https://iss.moex.com/iss/engines/stock/markets/bonds.xml?iss.meta=off  - справка по рынкам облигаций

    def __init__(self, sec_id):
        self.__sec_id = sec_id
        self.__checker = Check_security(sec_id)

        self.__market_data = dict()
        self.__securities = dict()
        self.__market_data_yields = dict()
        self.__make_request()

    def __make_request(self):
        share_or_bond = self.__checker.get_share_or_bond()
        board_id = self.__checker.get_board_id()

        request = F'https://iss.moex.com/iss/engines/stock/markets/{share_or_bond}/boards/{board_id}/' \
                  F'securities.json?iss.meta=off&securities={self.__sec_id}'
        response = requests.get(request)
        response = json.loads(response.text)

        self.__set_securities(response)
        self.__set_market_data(response)
        if share_or_bond == 'bonds':
            self.__set_market_data_yields(response)

    def __set_market_data(self, response):
        market_data_columns = response['marketdata']['columns']
        market_data_data = response['marketdata']['data'][0]

        for column in market_data_columns:
            index = list.index(market_data_columns, column)
            self.__market_data.update({column: market_data_data[index]})

    def __set_securities(self, response):
        securities_columns = response['securities']['columns']
        securities_data = response['securities']['data'][0]

        for column in securities_columns:
            index = list.index(securities_columns, column)
            self.__securities.update({column: securities_data[index]})

    def __set_market_data_yields(self, response):
        try:
            market_data_yields_columns = response['marketdata_yields']['columns']
            market_data_yields_data = response['marketdata_yields']['data'][0]

            for column in market_data_yields_columns:
                index = list.index(market_data_yields_columns, column)
                self.__market_data_yields.update({column: market_data_yields_data[index]})
        except IndexError:
            pass

    def get_market_data(self):
        return self.__market_data

    def get_securities(self):
        return self.__securities

    def get_market_data_yields(self):
        return self.__market_data_yields
