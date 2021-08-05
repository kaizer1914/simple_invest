from database_tables.msfo_table import Msfo_table


class Enter_company_data_ui:
    def __init__(self):
        try:
            ticker = str(input("Введите тикер компании: "))
            self.__msfo = Msfo_table(ticker)

            self.show_year()
            self.show_current_assets()
            self.show_non_current_assets()
            self.show_assets()
            self.show_equity()
            self.show_current_liabilities()
            self.show_non_current_liabilities()
            self.show_liabilities()
            self.show_net_debt()
            self.show_interest()
            self.show_sales()
            self.show_operating_income()
            self.show_net_income()
            self.show_ebitda()
            self.show_fcf()
            self.show_dividend()
        except ValueError:
            self.__init__()

    def show_year(self):
        try:
            year = int(input("Введите год финансового отчета: "))
            self.__msfo.set_year(year)
            self.__input_year = year
        except ValueError:
            self.show_year()

    def show_current_assets(self):
        try:
            current_assets = int(input("Введите значение текущих активов: "))
            self.__msfo.set_current_assets(current_assets, self.__input_year)
        except ValueError:
            self.show_current_assets()

    def show_non_current_assets(self):
        try:
            non_current_assets = int(input("Введите значение постоянных активов: "))
            self.__msfo.set_non_current_assets(non_current_assets, self.__input_year)
        except ValueError:
            self.show_non_current_assets()

    def show_assets(self):
        try:
            assets = int(input("Введите значение всего активов: "))
            self.__msfo.set_assets(assets, self.__input_year)
        except ValueError:
            self.show_assets()

    def show_equity(self):
        try:
            equity = int(input("Введите значение собственного капитала: "))
            self.__msfo.set_equity(equity, self.__input_year)
        except ValueError:
            self.show_equity()

    def show_current_liabilities(self):
        try:
            current_liabilities = int(input("Введите значение теущих обязательств: "))
            self.__msfo.set_current_liabilities(current_liabilities, self.__input_year)
        except ValueError:
            self.show_current_liabilities()

    def show_non_current_liabilities(self):
        try:
            non_current_liabilities = int(input("Введите значение долгосрочных обязательств: "))
            self.__msfo.set_non_current_liabilities(non_current_liabilities, self.__input_year)
        except ValueError:
            self.show_non_current_liabilities()

    def show_liabilities(self):
        try:
            liabilities = int(input("Введите значение всего обязательств: "))
            self.__msfo.set_liabilities(liabilities, self.__input_year)
        except ValueError:
            self.show_liabilities()

    def show_net_debt(self):
        try:
            net_debt = int(input("Введите значение чистого долга: "))
            self.__msfo.set_net_debt(net_debt, self.__input_year)
        except ValueError:
            self.show_net_debt()

    def show_interest(self):
        try:
            interest = int(input("Введите значение процентных платежей: "))
            self.__msfo.set_interest(interest, self.__input_year)
        except ValueError:
            self.show_interest()

    def show_sales(self):
        try:
            sales = int(input("Введите значение выручки: "))
            self.__msfo.set_sales(sales, self.__input_year)
        except ValueError:
            self.show_sales()

    def show_operating_income(self):
        try:
            operating_income = int(input("Введите значение операционной прибыли: "))
            self.__msfo.set_operating_income(operating_income, self.__input_year)
        except ValueError:
            self.show_operating_income()

    def show_net_income(self):
        try:
            net_income = int(input("Введите значение чистой прибыли: "))
            self.__msfo.set_net_income(net_income, self.__input_year)
        except ValueError:
            self.show_net_income()

    def show_ebitda(self):
        try:
            ebitda = int(input("Введите значение EBITDA: "))
            self.__msfo.set_ebitda(ebitda, self.__input_year)
        except ValueError:
            self.show_ebitda()

    def show_fcf(self):
        try:
            fcf = int(input("Введите значение свободного денежного потока: "))
            self.__msfo.set_fcf(fcf, self.__input_year)
        except ValueError:
            self.show_fcf()

    def show_dividend(self):
        try:
            dividend = int(input("Введите значение дивидендов: "))
            self.__msfo.set_dividend(dividend, self.__input_year)
        except ValueError:
            self.show_dividend()


if __name__ == '__main__':
    Enter_company_data_ui()
