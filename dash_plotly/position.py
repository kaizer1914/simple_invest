from dash import dcc, html, Output, Input
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Symbol, Scheme, Sign, Group

from dash_plotly.application import app
from vtb.position_report import PositionReport

url = '/position'  # Локальный адрес страницы

color_primary = '#bbdefb'
color_secondary = '#ffee58'

color_primary_light = '#eeffff'
color_primary_dark = '#8aacc8'

color_secondary_light = '#ffff8b'
color_secondary_dark = '#c9bc1f'

font = 'Arial'

upload_style = {
    'width': '97%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '20px',
    'backgroundColor': color_primary_light,
    'borderColor': color_secondary_dark,
    'font-family': font,
}

tab_style = {
    'font-family': font,
    'backgroundColor': color_primary_dark,
}

selected_tab_style = {
    'font-family': font,
    'border-color': color_primary_dark,
}

style_data_table = {
    'whiteSpace': 'normal',  # Перенос строк
    'height': '60px',
    'font-family': font,
    'textAlign': 'left',
    'padding': '20px',
}

style_data_conditional_shares_table = [
    {'if': {'row_index': 'odd'},  # Перебираем строки через одну
     'backgroundColor': color_primary_light},
    {'if': {'filter_query': '{income} > 0',  # Фильтр поиска по значению столбца
            'column_id': 'income'},
     'color': 'green'},
    {'if': {'filter_query': '{income} < 0',
            'column_id': 'income'},
     'color': 'red'},
]

style_data_conditional_bonds_table = [
    {'if': {'row_index': 'odd'},  # Перебираем строки через одну
     'backgroundColor': color_primary_light}]

style_header_table = {
    'height': '60px',
    'backgroundColor': color_primary,
    'font-family': font,
    'whiteSpace': 'normal',  # Перенос строк
    'textAlign': 'left',
    'padding': '10px',
}

sort_action_table = 'native'  # Включает сортировку по возрастанию и убыванию для всех столбцов

layout = html.Div([
    dcc.Upload(
        id='position-report-file',
        children=html.Div(['Перетащите или ', html.A('Выберите csv-файл')]),
        style=upload_style),
    dcc.Tabs([
        dcc.Tab(label='Акции и Фонды',
                children=[
                    html.Div(id='shares-report-table',
                             style={'margin': '20px'})
                ],
                style=tab_style,
                selected_style=selected_tab_style,
                ),
        dcc.Tab(label='Облигации',
                children=[
                    html.Div(id='bonds-report-table',
                             style={'margin': '20px'})
                ],
                style=tab_style,
                selected_style=selected_tab_style,
                ),
    ], style={'margin': '20px'}),
])


@app.callback(Output('shares-report-table', 'children'), Output('bonds-report-table', 'children'),
              Input('position-report-file', 'contents'))
def upload_position_report(contents):
    position_report = PositionReport()
    if contents is not None:
        position_report.save_to_db(contents)
    shares_data = position_report.get_shares_data()
    shares_table = DataTable(
        data=shares_data.to_dict('records'),
        columns=[
            dict(id='longname', name='Компания'),
            dict(id='ticker', name='Тикер'),
            dict(id='price', name='Цена', type='numeric',
                 format=Format(symbol=Symbol.yes, symbol_suffix=' ₽', group=Group.yes)),
            dict(id='count', name='Количество', type='numeric',
                 format=Format(symbol=Symbol.yes, symbol_suffix=' шт.', group=Group.yes)),
            dict(id='sum', name='Сумма', type='numeric', format=Format(precision=2, scheme=Scheme.decimal_si_prefix,
                                                                       group=Group.yes)),
            dict(id='income', name='Прибыль', type='numeric',
                 format=Format(scheme=Scheme.percentage_rounded, precision=2, sign=Sign.positive)),
        ],
        style_as_list_view=True,
        style_data=style_data_table,
        style_data_conditional=style_data_conditional_shares_table,
        style_header=style_header_table,
        cell_selectable=False,
        sort_action=sort_action_table,
    )

    bonds_data = position_report.get_bonds_data()
    bonds_table = DataTable(
        data=bonds_data.to_dict('records'),
        columns=[
            dict(id='longname', name='Наименование'),
            dict(id='current_price', name='Цена', type='numeric',
                 format=Format(symbol=Symbol.yes, symbol_suffix=' ₽', group=Group.yes, scheme=Scheme.decimal_integer)),
            dict(id='count', name='Количество', type='numeric',
                 format=Format(symbol=Symbol.yes, symbol_suffix=' шт.', group=Group.yes)),
            dict(id='couponperiod', name='Период купона', type='numeric'),
            dict(id='duration', name='Дюрация', type='numeric'),
            dict(id='effectiveyield', name='Эффективная доходность', type='numeric',
                 format=Format(symbol=Symbol.yes, symbol_suffix='%', group=Group.yes, precision=3)),
            dict(id='issuesize', name='Объём выпуска', type='numeric',
                 format=Format(precision=3, scheme=Scheme.decimal_si_prefix, group=Group.yes)),
            dict(id='enddate', name='Дата погашения')
        ],
        style_as_list_view=True,
        style_data=style_data_table,
        style_data_conditional=style_data_conditional_bonds_table,
        style_header=style_header_table,
        cell_selectable=False,
        sort_action=sort_action_table,
    )
    return shares_table, bonds_table
