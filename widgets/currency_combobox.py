from PyQt6.QtWidgets import QComboBox


class CurrencyComboBox(QComboBox):
    THOUSAND_RUBLES = 'тыс. ₽'
    MILLION_RUBLES = 'млн. ₽'
    BILLION_RUBLES = 'млрд. ₽'
    THOUSAND_DOLLARS = 'тыс. $'
    CURRENCY = 1000

    def __init__(self):
        super(CurrencyComboBox, self).__init__()
        self.addItem(self.THOUSAND_RUBLES)
        self.addItem(self.MILLION_RUBLES)
        self.addItem(self.BILLION_RUBLES)
        self.addItem(self.THOUSAND_DOLLARS)

        if self.currentText() == self.THOUSAND_RUBLES:
            self.CURRENCY = 1000
        elif self.currentText() == self.MILLION_RUBLES:
            self.CURRENCY = 1000000
        elif self.currentText() == self.BILLION_RUBLES:
            self.CURRENCY = 1000000000
        elif self.currentText() == self.THOUSAND_DOLLARS:
            self.CURRENCY = 1000 * 1  # курс доллара
