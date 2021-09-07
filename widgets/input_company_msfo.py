import sys

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QApplication, QPushButton

from tables.msfo_table import MsfoTable
from widgets.currency_combobox import CurrencyComboBox


class InputCompanyMSFO(QWidget):
    def __init__(self):
        super().__init__()
        ticker_label = QLabel('Тикер')
        year_label = QLabel('Год')
        current_assets_label = QLabel('Текущие активы')
        non_current_assets_label = QLabel('Постоянные активы')
        assets_label = QLabel('Активы')
        equity_label = QLabel('Собственный капитал')
        current_liabilities_label = QLabel('Текущие обязательства')
        non_current_liabilities_label = QLabel('Долгосрочные обязательства')
        liabilities_label = QLabel('Обязательства')
        net_debt_label = QLabel('Чистый долг')
        interest_label = QLabel('Процентные платежи')
        sales_label = QLabel('Выручка')
        operating_income_label = QLabel('Операционная прибыль')
        net_income_label = QLabel('Чистая прибыль')
        ebitda_label = QLabel('EBITDA')
        fcf_label = QLabel('FCF')
        dividend_label = QLabel('Дивиденды')

        self.__currency_combobox = CurrencyComboBox()
        self.__ticker_line_edit = QLineEdit()
        self.__year_line_edit = QLineEdit()
        self.__current_assets_line_edit = QLineEdit()
        self.__non_current_assets_line_edit = QLineEdit()
        self.__assets_line_edit = QLineEdit()
        self.__equity_line_edit = QLineEdit()
        self.__current_liabilities_line_edit = QLineEdit()
        self.__non_current_liabilities_line_edit = QLineEdit()
        self.__liabilities_line_edit = QLineEdit()
        self.__net_debt_line_edit = QLineEdit()
        self.__interest_line_edit = QLineEdit()
        self.__sales_line_edit = QLineEdit()
        self.__operating_income_line_edit = QLineEdit()
        self.__net_income_line_edit = QLineEdit()
        self.__ebitda_line_edit = QLineEdit()
        self.__fcf_line_edit = QLineEdit()
        self.__dividend_line_edit = QLineEdit()

        self.__ticker_line_edit.setInputMask('>AAAAA')
        self.__year_line_edit.setInputMask('9999')
        self.__current_assets_line_edit.setInputMask('#999999999')
        self.__non_current_assets_line_edit.setInputMask('#999999999')
        self.__assets_line_edit.setInputMask('#999999999')
        self.__equity_line_edit.setInputMask('#999999999')
        self.__current_liabilities_line_edit.setInputMask('#999999999')
        self.__non_current_liabilities_line_edit.setInputMask('#999999999')
        self.__liabilities_line_edit.setInputMask('#999999999')
        self.__net_debt_line_edit.setInputMask('#999999999')
        self.__interest_line_edit.setInputMask('#999999999')
        self.__sales_line_edit.setInputMask('999999999')
        self.__operating_income_line_edit.setInputMask('#999999999')
        self.__net_income_line_edit.setInputMask('#999999999')
        self.__ebitda_line_edit.setInputMask('999999999')
        self.__fcf_line_edit.setInputMask('#999999999')
        self.__dividend_line_edit.setInputMask('999999999')

        ok_button = QPushButton('Сохранить')
        cancel_button = QPushButton('Отмена')
        # ok_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # cancel_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        ok_button.clicked.connect(self.ok_button_clicked)
        cancel_button.clicked.connect(self.cancel_button_clicked)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(ticker_label, 0, 0)
        layout.addWidget(self.__ticker_line_edit, 0, 1)
        layout.addWidget(year_label, 1, 0)
        layout.addWidget(self.__year_line_edit, 1, 1)
        layout.addWidget(self.__currency_combobox, 2, 1)

        layout.addWidget(current_assets_label, 3, 0)
        layout.addWidget(self.__current_assets_line_edit, 3, 1)
        layout.addWidget(non_current_assets_label, 4, 0)
        layout.addWidget(self.__non_current_assets_line_edit, 4, 1)
        layout.addWidget(assets_label, 5, 0)
        layout.addWidget(self.__assets_line_edit, 5, 1)
        layout.addWidget(equity_label, 6, 0)
        layout.addWidget(self.__equity_line_edit, 6, 1)
        layout.addWidget(current_liabilities_label, 7, 0)
        layout.addWidget(self.__current_liabilities_line_edit, 7, 1)
        layout.addWidget(non_current_liabilities_label, 8, 0)
        layout.addWidget(self.__non_current_liabilities_line_edit, 8, 1)
        layout.addWidget(liabilities_label, 9, 0)
        layout.addWidget(self.__liabilities_line_edit, 9, 1)

        layout.addWidget(net_debt_label, 10, 0)
        layout.addWidget(self.__net_debt_line_edit, 10, 1)
        layout.addWidget(interest_label, 11, 0)
        layout.addWidget(self.__interest_line_edit, 11, 1)

        layout.addWidget(sales_label, 12, 0)
        layout.addWidget(self.__sales_line_edit, 12, 1)
        layout.addWidget(operating_income_label, 13, 0)
        layout.addWidget(self.__operating_income_line_edit, 13, 1)
        layout.addWidget(net_income_label, 14, 0)
        layout.addWidget(self.__net_income_line_edit, 14, 1)

        layout.addWidget(ebitda_label, 15, 0)
        layout.addWidget(self.__ebitda_line_edit, 15, 1)
        layout.addWidget(fcf_label, 16, 0)
        layout.addWidget(self.__fcf_line_edit, 16, 1)
        layout.addWidget(dividend_label, 17, 0)
        layout.addWidget(self.__dividend_line_edit, 17, 1)

        layout.addWidget(ok_button, 18, 0)
        layout.addWidget(cancel_button, 18, 1)

        self.setLayout(layout)
        self.show()

    def ok_button_clicked(self):
        currency = self.__currency_combobox.get_currency()

        ticker = str(self.__ticker_line_edit.text())
        year = int(self.__year_line_edit.text())
        current_assets = int(self.__current_assets_line_edit.text()) * currency
        non_current_assets = int(self.__non_current_assets_line_edit.text()) * currency
        assets = int(self.__assets_line_edit.text()) * currency
        equity = int(self.__equity_line_edit.text()) * currency
        current_liabilities = int(self.__current_liabilities_line_edit.text()) * currency
        non_current_liabilities = int(self.__non_current_liabilities_line_edit.text()) * currency
        liabilities = int(self.__liabilities_line_edit.text()) * currency
        interest = int(self.__interest_line_edit.text()) * currency
        net_debt = int(self.__net_debt_line_edit.text()) * currency
        sales = int(self.__sales_line_edit.text()) * currency
        operating_income = int(self.__operating_income_line_edit.text()) * currency
        net_income = int(self.__net_income_line_edit.text()) * currency
        ebitda = int(self.__ebitda_line_edit.text()) * currency
        fcf = int(self.__fcf_line_edit.text()) * currency
        dividend = int(self.__dividend_line_edit.text()) * currency

        table = MsfoTable(ticker)
        table.set_year(year)
        table.set_current_assets(current_assets, year)
        table.set_non_current_assets(non_current_assets, year)
        table.set_assets(assets, year)
        table.set_equity(equity, year)
        table.set_current_liabilities(current_liabilities, year)
        table.set_non_current_liabilities(non_current_liabilities, year)
        table.set_liabilities(liabilities, year)
        table.set_interest(interest, year)
        table.set_net_debt(net_debt, year)
        table.set_sales(sales, year)
        table.set_operating_income(operating_income, year)
        table.set_net_income(net_income, year)
        table.set_ebitda(ebitda, year)
        table.set_fcf(fcf, year)
        table.set_dividend(dividend, year)
        self.close()

    def cancel_button_clicked(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = InputCompanyMSFO()
    sys.exit(app.exec())
