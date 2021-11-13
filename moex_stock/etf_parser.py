'''
https://www.moex.com/msn/etf
Спарсить страничку с целью выяснения etf и бпиф Московской биржи по классу активов
и последующего сохранения в БД
'''

import pandas
import requests
from bs4 import BeautifulSoup


class EtfParser:
    columns = {
        1: 'fund',
        2: 'provider',
        3: 'base_asset',
        4: 'currency',
        5: 'type',
        6: 'ticker',
    }

    def __init__(self):
        url = 'https://www.moex.com/msn/etf'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.findAll('table')[1].tbody
        rows = table.find_all('tr')
        data = list()

        for row in rows:
            cols = row.find_all('td')
            cols = [element.text.strip() for element in cols]
            data.append([element for element in cols if element])
        data.pop(0)

        bonds_index = 0
        cash_index = 0
        shares_index = 0
        products_index = 0
        gold_index = 0
        mix_assets_index = 0

        for row in data:
            if row[0] == 'Облигации/Еврооблигации':
                bonds_index = data.index(row)
            elif row[0] == 'Денежный рынок':
                cash_index = data.index(row)
            elif row[0] == 'Акции':
                shares_index = data.index(row)
            elif row[0] == 'Товары':
                products_index = data.index(row)
            elif row[0] == 'Золото':
                gold_index = data.index(row)
            elif row[0] == 'Смешанные активы':
                mix_assets_index = data.index(row)
            else:
                row[1] = row[1].replace('\n', '').replace('\r', '').replace('\t', '')
                row[2] = row[2].replace('\n', '').replace('\r', '').replace('\t', '')
                row[3] = row[3].replace('\n', '').replace('\r', '').replace('\t', '')

        self.__bonds_list = data[bonds_index + 1:cash_index]
        self.__cash_list = data[cash_index + 1:shares_index]
        self.__shares_list = data[shares_index + 1:products_index]
        self.__gold_list = data[gold_index + 1:mix_assets_index]
        self.__mix_assets_list = data[mix_assets_index + 1:]

    def get_bonds_df(self):
        df = pandas.DataFrame(self.__bonds_list)
        df = df.rename(self.columns, axis='columns')
        df = df.drop(0, axis='columns')  # Удаляем номера строк
        df = df.drop(7, axis='columns')  # Удаляем бесполезную колонку
        return df

    def get_cash_df(self):
        df = pandas.DataFrame(self.__cash_list)
        df = df.rename(self.columns, axis='columns')
        df = df.drop(0, axis='columns')  # Удаляем номера строк
        df = df.drop(7, axis='columns')  # Удаляем бесполезную колонку
        return df

    def get_shares_df(self):
        df = pandas.DataFrame(self.__shares_list)
        df = df.rename(self.columns, axis='columns')
        df = df.drop(0, axis='columns')  # Удаляем номера строк
        df = df.drop(7, axis='columns')  # Удаляем бесполезную колонку
        return df

    def get_gold_df(self):
        df = pandas.DataFrame(self.__gold_list)
        df = df.rename(self.columns, axis='columns')
        df = df.drop(0, axis='columns')  # Удаляем номера строк
        df = df.drop(7, axis='columns')  # Удаляем бесполезную колонку
        return df

    def get_mix_assets_df(self):
        df = pandas.DataFrame(self.__mix_assets_list)
        df = df.rename(self.columns, axis='columns')
        df = df.drop(0, axis='columns')  # Удаляем номера строк
        df = df.drop(7, axis='columns')  # Удаляем бесполезную колонку
        return df
