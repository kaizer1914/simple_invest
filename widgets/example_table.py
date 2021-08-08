import sys

from PyQt6.QtWidgets import QWidget, QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout

from tables.msfo_table import Msfo_table


class ExampleTable(QWidget):
    def __init__(self, ticker):
        super(ExampleTable, self).__init__()
        table = Msfo_table(ticker)
        layout = QVBoxLayout()

        table_widget = QTableWidget(1, table.get_count_years())
        table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        table_widget.setHorizontalHeaderLabels(table.get_all_years())

        for year in table.get_all_years():
            table_widget.setItem(0, 0, QTableWidgetItem(str(table.get_sales(year))))

        layout.addWidget(table_widget)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ExampleTable('AKRN')
    sys.exit(app.exec())
