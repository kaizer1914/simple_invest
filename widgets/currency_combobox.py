from PyQt6.QtWidgets import QComboBox


class CurrencyComboBox(QComboBox):
    THOUSAND_RUBLES = 'тыс. ₽'
    MILLION_RUBLES = 'млн. ₽'
    BILLION_RUBLES = 'млрд. ₽'
    THOUSAND_DOLLARS = 'тыс. $'

    def __init__(self):
        super(CurrencyComboBox, self).__init__()
        self.addItem(self.THOUSAND_RUBLES)
        self.addItem(self.MILLION_RUBLES)
        self.addItem(self.BILLION_RUBLES)
        self.addItem(self.THOUSAND_DOLLARS)
        self.__currency = 1000
        self.currentTextChanged.connect(self.on_change_click)

    def get_currency(self):
        return self.__currency

    def on_change_click(self, text):
        if text == self.THOUSAND_RUBLES:
            self.__currency = 1000
        elif text == self.MILLION_RUBLES:
            self.__currency = 1000000
        elif text == self.BILLION_RUBLES:
            self.__currency = 1000000000
        elif text == self.THOUSAND_DOLLARS:
            self.__currency = 1000 * 74  # курс доллара
