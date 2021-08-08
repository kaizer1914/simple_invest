from moex_stock.moex_data_parser import Moex_data_parser
from tables.bonds_table import Bonds_table
from tables.etf_table import Etf_table
from tables.securities_table import Securities_table
from tables.shares_table import Shares_table
from vtb_position_report import Vtb_position_report


class Analyser:
    __percent_format = '.2%'
    __money_format = ',.2f'

    __securities_table = Securities_table()
    __shares_table = Shares_table()
    __bonds_table = Bonds_table()
    __etf_table = Etf_table()

    def update_stock_info(self):
        for sec_id in self.__securities_table.get_sec_id():
            security = Moex_data_parser(sec_id)
            if security.get_sec_type() == '1' or security.get_sec_type() == '2' or security.get_sec_type() == 'D':
                self.__shares_table.add(security.get_sec_id(), security.get_sec_name(), security.get_short_name(),
                                        security.get_isin(), security.get_share_last_price(),
                                        security.get_sec_type(),
                                        security.get_list_level(), security.get_share_lot_size(),
                                        security.get_issue_size())
                if security.get_sec_type() == '2':
                    usual_share = Moex_data_parser(sec_id[:-1])
                    self.__shares_table.add(usual_share.get_sec_id(), usual_share.get_sec_name(),
                                            usual_share.get_short_name(),
                                            usual_share.get_isin(), usual_share.get_share_last_price(),
                                            usual_share.get_sec_type(), usual_share.get_list_level(),
                                            usual_share.get_share_lot_size(), usual_share.get_issue_size())
            elif security.get_sec_type() == '3' or security.get_sec_type() == '4' or security.get_sec_type() == '5' or \
                    security.get_sec_type() == '6' or security.get_sec_type() == '7' or security.get_sec_type() == '8' \
                    or security.get_sec_type() == 'C':
                self.__bonds_table.add(security.get_sec_id(), security.get_sec_name(), security.get_short_name(),
                                       security.get_isin(), security.get_sec_type(), security.get_list_level(),
                                       security.get_bond_price(), security.get_bond_lot_value(), security.get_nkd(),
                                       security.get_coupon_value(), security.get_coupon_period(),
                                       security.get_coupon_percent(),
                                       security.get_next_coupon(), security.get_mat_date(),
                                       security.get_offer_date(),
                                       security.get_yield_date_type(), security.get_effective_yield(),
                                       security.get_yield_date(),
                                       security.get_duration())
            else:
                self.__etf_table.add(security.get_sec_id(), security.get_sec_name(), security.get_short_name(),
                                     security.get_isin(), security.get_share_last_price(), security.get_sec_type(),
                                     security.get_list_level(), security.get_share_lot_size())

    def update_broker_report(self, file_report='/home/kirill/Загрузки/OlbPosDetailReport.csv'):
        position_report = Vtb_position_report()
        position_report.load_from_file(file_report)
        position_report.save_to_database(self.__securities_table)

    def __get_total(self):
        return self.__shares_table.get_total_cost() + float(self.__bonds_table.get_total_cost()) + \
               self.__etf_table.get_total_cost()


if __name__ == '__main__':
    analyser = Analyser()
    analyser.update_broker_report()
    analyser.update_stock_info()
