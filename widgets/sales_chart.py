import sys

from PyQt6.QtCharts import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QSizePolicy

from tables.msfo_table import Msfo_table
from widgets.currency_combobox import CurrencyComboBox


class SalesChart(QWidget):
    def __init__(self, ticker):
        super(SalesChart, self).__init__()
        self.__table = Msfo_table(ticker)
        self.currency_combobox = CurrencyComboBox()
        self.currency_combobox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.currency_combobox.currentTextChanged.connect(self.__on_change_event)

        self.__chart_view = QChartView()
        self.__create_chart()

        layout = QVBoxLayout()
        layout.addWidget(self.__chart_view)
        layout.addWidget(self.currency_combobox)

        self.setLayout(layout)
        self.show()

    def __create_chart(self):
        chart = QChart()
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        chart.addSeries(self.__create_series())
        chart.addAxis(self.__create_axis_x(), Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(self.__create_axis_y(), Qt.AlignmentFlag.AlignLeft)
        self.__chart_view.setChart(chart)

    def __create_series(self):
        self.__sales = list()
        for year in self.__table.get_all_years():
            self.__sales.append(self.__table.get_sales(year) / self.currency_combobox.get_currency())

        sales_set = QBarSet('Выручка')
        sales_set.hovered.connect(self.on_hovered)
        sales_set.append(self.__sales)

        series = QBarSeries()
        series.append(sales_set)
        return series

    def __create_axis_x(self):
        axis_x = QBarCategoryAxis()
        axis_x.append(self.__table.get_all_years())
        axis_x.setGridLineVisible(False)
        return axis_x

    def __create_axis_y(self):
        max = list()
        for year in self.__table.get_all_years():
            max.append(self.__table.get_sales(year) / self.currency_combobox.get_currency())
        max.sort()

        axis_y = QValueAxis()
        axis_y.setMax(max[-1])
        axis_y.setLabelFormat('%.0f')
        return axis_y

    def on_hovered(self, status, index):
        if status:
            tooltip = str(int(self.__sales[index]))
            self.__chart_view.setToolTip(tooltip)

    # переопределен метод currency combo box
    def __on_change_event(self, text):
        self.currency_combobox.on_change_click(text)
        self.__create_chart()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SalesChart('AKRN')
    sys.exit(app.exec())
