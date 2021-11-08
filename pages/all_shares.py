from dash_bootstrap_components import Table

from moex_stock.shares import SharesMarket

shares_market = SharesMarket()
dataframe = shares_market.update_stock_data()

url = '/all-shares'

# layout = DataTable(
#     id='shares_table',
#     columns=[{"name": col, "id": col} for col in dataframe.columns],
#     data=dataframe.to_dict('records'),
#     style_as_list_view=True,
#     style_cell={'textAlign': 'left'},
# )

table = Table.from_dataframe(dataframe, striped=True, bordered=True, hover=True, index=True)
layout = table
