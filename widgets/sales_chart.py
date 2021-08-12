import sys

from PyQt6.QtCharts import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout

from tables.msfo_table import Msfo_table
from widgets.currency_combobox import CurrencyComboBox


class SalesChart(QWidget):
    def __init__(self, ticker):
        super(SalesChart, self).__init__()
        self.__table = Msfo_table(ticker)
        self.__currency_combobox = CurrencyComboBox()
        self.__currency_combobox.currentTextChanged.connect(self.__on_change_event)

        self.__chart_view = QChartView()
        self.__create_chart()

        layout = QVBoxLayout()
        layout.addWidget(self.__chart_view)
        layout.addWidget(self.__currency_combobox)

        self.setLayout(layout)
        self.show()

    def __create_chart(self):
        chart = QChart()
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.addSeries(self.__create_series())
        chart.addAxis(self.__create_axis_x(), Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(self.__create_axis_y(), Qt.AlignmentFlag.AlignLeft)
        self.__chart_view.setChart(chart)

    def __create_series(self):
        sales = list()
        for year in self.__table.get_all_years():
            sales_year = self.__table.get_sales(year) / self.__currency_combobox.CURRENCY
            sales.append(sales_year)

        sales_set = QBarSet('Выручка')
        sales_set.append(sales)

        series = QBarSeries()
        series.append(sales_set)
        return series

    def __create_axis_x(self):
        axis_x = QBarCategoryAxis()
        axis_x.append(self.__table.get_all_years())
        return axis_x

    def __create_axis_y(self):
        min_max = list()
        for year in self.__table.get_all_years():
            min_max.append(self.__table.get_sales(year) / self.__currency_combobox.CURRENCY)
        min_max.sort()

        axis_y = QValueAxis()
        axis_y.setRange(min_max[0], min_max[-1])
        axis_y.applyNiceNumbers()
        axis_y.setLabelFormat('%.0f')
        return axis_y

    def __on_change_event(self, text):
        if text == self.__currency_combobox.THOUSAND_RUBLES:
            self.__currency_combobox.CURRENCY = 1000
        elif text == self.__currency_combobox.MILLION_RUBLES:
            self.__currency_combobox.CURRENCY = 1000000
        elif text == self.__currency_combobox.BILLION_RUBLES:
            self.__currency_combobox.CURRENCY = 1000000000
        elif text == self.__currency_combobox.THOUSAND_DOLLARS:
            self.__currency_combobox.CURRENCY = 1000 * 1  # курс доллара
        self.__create_chart()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SalesChart('AKRN')
    sys.exit(app.exec())
