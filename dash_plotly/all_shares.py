from dash.dash_table import DataTable

from moex_stock.shares_funds import SharesMarket

shares_market = SharesMarket()
dataframe = shares_market.update_stock_data()

url = '/all-shares'

layout = DataTable(
    id='shares_table',
    columns=[{"name": col, "id": col} for col in dataframe.columns],
    data=dataframe.to_dict('records'),
    style_as_list_view=True,
    style_cell={'textAlign': 'left'},
)
