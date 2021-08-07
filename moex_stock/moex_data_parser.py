from moex_stock_data.moex_stock_data import Moex_stock_data


class Moex_data_parser:
    def __init__(self, sec_id):
        self.__data = Moex_stock_data(sec_id)

    def get_sec_id(self):
        return self.__data.get_securities().get('SECID')

    def get_short_name(self):
        short_name = self.__data.get_securities().get('SHORTNAME')
        short_name = str.replace(short_name, "'", "")
        return short_name

    def get_sec_name(self):
        sec_name = self.__data.get_securities().get('SECNAME')
        sec_name = str.replace(sec_name, "'", "")
        return sec_name

    def get_isin(self):
        return self.__data.get_securities().get('ISIN')

    def get_issue_size(self):
        return int(self.__data.get_securities().get('ISSUESIZE'))

    def get_share_last_price(self):
        return float(self.__data.get_market_data().get('LAST'))

    def get_sec_type(self):
        return self.__data.get_securities().get('SECTYPE')

    def get_list_level(self):
        return int(self.__data.get_securities().get('LISTLEVEL'))

    def get_coupon_value(self):
        return float(self.__data.get_securities().get('COUPONVALUE'))

    def get_next_coupon(self):
        return self.__data.get_securities().get('NEXTCOUPON')

    def get_nkd(self):
        return float(self.__data.get_securities().get('ACCRUEDINT'))

    def get_mat_date(self):
        return self.__data.get_securities().get('MATDATE')

    def get_coupon_period(self):
        return int(self.__data.get_securities().get('COUPONPERIOD'))

    def get_offer_date(self):
        offer_date = self.__data.get_securities().get('OFFERDATE')
        if offer_date is None:
            return self.get_mat_date()
        else:
            return offer_date

    def get_coupon_percent(self):
        coupon_percent = self.__data.get_securities().get('COUPONPERCENT')
        if coupon_percent is None:
            return 0
        else:
            return coupon_percent

    def get_bond_lot_value(self):
        return int(self.__data.get_securities().get('LOTVALUE'))

    def get_share_lot_size(self):
        return int(self.__data.get_securities().get('LOTSIZE'))

    # Не рекомендуется использоваьть
    def get_market_cap(self):
        market_cap = self.get_issue_size() * self.get_share_last_price()
        if self.get_sec_type() == '2':
            # request = F'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/' \
            #           F'securities.json?iss.meta=off&securities={self.get_sec_id()[:-1]}'
            # response = requests.get(request)
            # response = json.loads(response.text)
            #
            # securities_columns = response['securities']['columns']
            # securities_data = response['securities']['data'][0]
            #
            # market_data_columns = response['marketdata']['columns']
            # market_data_data = response['marketdata']['data'][0]
            #
            # issue_size = list.index(securities_columns, 'ISSUESIZE')
            # last_price = list.index(market_data_columns, 'LAST')

            usual_share = Moex_data_parser(Moex_stock_data(self.get_sec_id()[:-1]))
            pref_cap = self.get_issue_size() * self.get_share_last_price()
            usual_cap = usual_share.get_share_last_price() * usual_share.get_issue_size()
            market_cap = int(usual_cap + pref_cap)
        return market_cap

    def get_yield_date_type(self):
        # MATDATE or OFFERDATE
        return self.__data.get_market_data_yields().get('YIELDDATETYPE')

    def get_effective_yield(self):
        return float(self.__data.get_market_data_yields().get('EFFECTIVEYIELD'))

    def get_duration(self):
        return int(self.__data.get_market_data_yields().get('DURATION'))

    def get_yield_date(self):
        return self.__data.get_market_data_yields().get('YIELDDATE')

    def get_bond_price(self):
        return float(self.__data.get_market_data_yields().get('PRICE'))
