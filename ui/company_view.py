from PyQt6.QtWidgets import QWidget

from database_tables.msfo_table import Msfo_table


class Company_View(QWidget):
    def __init__(self, ticker):
        super(Company_View, self).__init__()
        table = Msfo_table(ticker)

