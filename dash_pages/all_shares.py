from dash.dash_table import DataTable

from moex_stock.shares import SharesMarket

dataframe = SharesMarket.update_stock_data()
shares_df = dataframe[dataframe['sectype'].isin(['usual', 'pref', 'dr'])]

table_bg = '#073642'
table_striped_bg = '#13404b'
table_active_bg = '#204a55'
table_hover_bg = '#1a4550'
border_color = '#204a55'

url = '/all-shares'
table_id = 'all-shares-table'

layout = DataTable(
    columns=[
        dict(id='ticker', name='Тикер'),
        dict(id='longname', name='Наименование'),
        dict(id='current_price', name='Текущая цена'),
        dict(id='lotsize', name='Размер лота'),
        dict(id='market_cap', name='Капитализация'),
        dict(id='issuesize', name='Количество акций'),
    ],
    style_cell={
        'scrollbarColor': table_bg,
        'padding': '10px',
        'textAlign': 'left',
        'whiteSpace': 'normal',
        'backgroundColor': table_bg,
        'fontFamily': '"Source Sans Pro", BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, '
                      '"Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
        'border': 'thin hidden ' + border_color,
    },
    style_data_conditional=[
        {'if': {'row_index': 'odd'},
         'backgroundColor': table_striped_bg},
        {'if': {'state': 'active'},  # 'active' | 'selected'
         'backgroundColor': table_active_bg,
         'border': 'thick solid ' + border_color}
    ],
    style_data={'paddingLeft': '20px'},
    style_header={
        'fontWeight': 'bold',
        'border': 'thick solid ' + border_color,
        'backgroundColor': table_active_bg,
    },
    id=table_id,
    data=shares_df.to_dict('records'),
    sort_action='native',
    style_as_list_view=True,
    page_size=15,
)
