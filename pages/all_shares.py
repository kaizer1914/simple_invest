from dash_bootstrap_components import Table

from moex_stock.shares import SharesMarket

shares_market = SharesMarket()
dataframe = shares_market.update_stock_data()

url = '/all-shares'

table = Table.from_dataframe(dataframe, striped=True, bordered=True, hover=True, index=True)
layout = table
