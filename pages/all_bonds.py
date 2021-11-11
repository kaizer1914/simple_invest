from dash_bootstrap_components import Table

from moex_stock.bonds import BondsMarket

dataframe = BondsMarket.update_stock_data()

url = '/all-bonds'

table = Table.from_dataframe(dataframe, striped=True, hover=True)
layout = table
