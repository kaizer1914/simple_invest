from dash_bootstrap_components import Table

from moex_stock.shares import SharesMarket

dataframe = SharesMarket.update_stock_data()

url = '/all-shares'

table = Table.from_dataframe(dataframe, striped=True, hover=True)
layout = table
