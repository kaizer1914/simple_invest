import plotly.express as px
from dash import dcc, html, Output, Input
from dash.dcc import Graph
from dash_bootstrap_components import Tabs, Tab, Row, Table, Alert, Col

from pages.application import app
from vtb.position_report import PositionReport

url = '/position'  # Локальный адрес страницы

upload_id = 'position-report-file'
shares_tab_id = 'shares-tab-report'
bonds_tab_id = 'bonds-tab-report'
total_tab_id = 'total-tab-report'

upload_style = {
    'width': '100%',
    'height': '60px',
    'lineHeight': '60px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'marginBottom': '20px',
    'marginTop': '20px',
}

layout = Row([
    dcc.Upload(
        id=upload_id,
        children=html.Div(['Перетащите или ', html.A('Выберите csv-файл')]),
        style=upload_style,
    ),
    Tabs([
        Tab(label='Общий отчет', children=[Row(id=total_tab_id)]),
        Tab(label='Акции', children=[Row(id=shares_tab_id)]),
        Tab(label='Облигации', children=[Row(id=bonds_tab_id)]),
    ]),
])


def add_share_sum_part(position_report) -> Col:
    shares_sum_df = position_report.get_shares_report(['name', 'ticker', 'current_sum', 'change_sum'])
    pie_fig = px.pie(shares_sum_df, values='current_sum', names='name', hover_data=['ticker'],
                     labels={'ticker': 'Тикер',
                             'current_sum': 'Текущая сумма',
                             'name': 'Наименование'},
                     title='Распределение по долям',
                     template='plotly_dark')
    bar_fig = px.bar(shares_sum_df, x='ticker', y='current_sum', color='change_sum', )

    pie_graph = Graph(figure=pie_fig, style={'marginTop': '20px'})
    bar_graph = Graph(figure=bar_fig, style={'marginTop': '20px'})
    return Col([pie_graph, bar_graph])


def add_shares_income_part(position_report) -> Graph:
    shares_income_df = position_report.get_shares_report(['name', 'ticker', 'change_sum', 'current_sum'])
    bar_fig = px.bar(shares_income_df, x='ticker', y='change_sum', color='change_sum',
                     hover_data=['name', 'current_sum'],
                     labels={'current_sum': 'Текущая сумма',
                             'name': 'Наименование',
                             'ticker': 'Тикер',
                             'change_sum': 'Доходность'},
                     title='Распределение по доходности',
                     template='plotly_dark')
    bar_graph = Graph(figure=bar_fig, style={'marginTop': '20px'})
    return bar_graph


@app.callback(Output(total_tab_id, 'children'), Output(shares_tab_id, 'children'), Output(bonds_tab_id, 'children'),
              Input(upload_id, 'contents'))
def upload_position_report(contents):
    if contents is None:
        alert = Alert(['Нет данных'], color='dark', style={'marginTop': '20px'})
        return alert, alert, alert
    elif contents is not None:
        position_report = PositionReport(contents)

        bonds_df = position_report.get_bonds_report()
        bonds_table = Table.from_dataframe(bonds_df, striped=True, hover=True)
        bonds_part = Row([bonds_table])

        shares_sum_part = add_share_sum_part(position_report)
        shares_income_part = add_shares_income_part(position_report)

        shares_report = Row([shares_sum_part, shares_income_part])

        total_report = html.P('Не готов')
        return total_report, shares_report, bonds_part