# Загружаем и парсим отчет по позциям из втб на любую дату, сохраняем результат в БД
import csv

from tables.securities_table import Securities_table


class Vtb_position_report:

    def __init__(self):
        self.__sec_count = dict()
        self.__sec_buy_price = dict()

    def load_from_file(self, file: str):
        with open(file) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                sec_id = row['textBox14']
                count = int(''.join(row['textBox22'].split()))
                buy_price = float(''.join(row['textBox21'].split()))

                self.__sec_count.update({sec_id: count})
                self.__sec_buy_price.update(({sec_id: buy_price}))

    def save_to_database(self, table: Securities_table):
        table.clear_table()
        for sec_id, count in self.__sec_count.items():
            table.add(sec_id, count, self.__sec_buy_price[sec_id])
