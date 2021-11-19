from dash.dash_table import DataTable

from moex_stock.shares import SharesMarket

dataframe = SharesMarket.update_stock_data()
shares_df = dataframe[dataframe['sectype'].isin(['usual', 'pref', 'dr'])]


url = '/all-shares'
table_id = 'all-shares-table'

layout = DataTable(
    id=table_id,
    data=shares_df.to_dict('records'),
    columns=[
        dict(id='ticker', name='Тикер'),
        dict(id='longname', name='Наименование'),
        dict(id='current_price', name='Текущая цена'),
        dict(id='lotsize', name='Размер лота'),
        dict(id='market_cap', name='Капитализация'),
        dict(id='issuesize', name='Количество акций'),
    ],
    style_cell={'textAlign': 'left'},
    style_data={'whiteSpace': 'normal'},
    page_size=15,
)
