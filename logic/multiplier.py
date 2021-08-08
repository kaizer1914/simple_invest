from moex_stock.moex_data_parser import Moex_data_parser
from tables.msfo_table import Msfo_table


class Multiplier:
    def __init__(self, sec_id):
        self.__market_cap = Moex_data_parser(sec_id).get_market_cap()
        self.__msfo_table = Msfo_table(sec_id)

    def get_earnings_to_price(self, year: int):
        earnings_to_price = round(self.__msfo_table.get_net_income(year) / self.__market_cap * 100, 2)
        return earnings_to_price

    def get_fcf_to_price(self, year: int):
        fcf_to_price = round(self.__msfo_table.get_fcf(year) / self.__market_cap * 100, 2)
        return fcf_to_price

    def get_dividend_to_price(self, year: int):
        dividend_to_price = round(self.__msfo_table.get_dividend(year) / self.__market_cap * 100, 2)
        return dividend_to_price

    def get_price_to_sales(self, year: int):
        price_to_sales = round(self.__market_cap / self.__msfo_table.get_sales(year), 2)
        return price_to_sales

    def get_price_to_book_value(self, year: int):
        price_to_book_value = round(self.__market_cap / self.__msfo_table.get_equity(year), 2)
        return price_to_book_value

    def get_ev_to_ebitda(self, year: int):
        ev_to_ebitda = round((self.__market_cap + self.__msfo_table.get_net_debt(year)) /
                             self.__msfo_table.get_ebitda(year), 2)
        return ev_to_ebitda

    def get_roa(self, year: int):
        roa = round(self.__msfo_table.get_operating_income(year) / self.__msfo_table.get_assets(year) * 100, 2)
        return roa

    def get_roe(self, year: int):
        roe = round(self.__msfo_table.get_net_income(year) / self.__msfo_table.get_equity(year) * 100, 2)
        return roe

    def get_ros(self, year: int):
        ros = round(self.__msfo_table.get_operating_income(year) / self.__msfo_table.get_sales(year) * 100, 2)
        return ros

    def get_asset_turnover(self, year: int):
        asset_turnover = round(self.__msfo_table.get_sales(year) / self.__msfo_table.get_assets(year), 2)
        return asset_turnover

    def get_net_debt_to_ebitda(self, year: int):
        net_debt_to_ebitda = round(self.__msfo_table.get_net_debt(year) / self.__msfo_table.get_ebitda(year), 2)
        return net_debt_to_ebitda

    def get_interest_cover(self, year: int):
        interest_cover = round(self.__msfo_table.get_operating_income(year) / self.__msfo_table.get_interest(year), 2)
        return interest_cover

    def get_equity_to_liabilities(self, year: int):
        equity_to_liabilities = round(self.__msfo_table.get_equity(year) / self.__msfo_table.get_liabilities(year), 2)
        return equity_to_liabilities

    def get_ebitda_margin(self, year: int):
        ebitda_margin = round(self.__msfo_table.get_ebitda(year) / self.__msfo_table.get_sales(year) * 100, 2)
        return ebitda_margin

    def get_current_ratio(self, year: int):
        current_ratio = round(self.__msfo_table.get_current_assets(year) /
                              self.__msfo_table.get_current_liabilities(year), 2)
        return current_ratio
