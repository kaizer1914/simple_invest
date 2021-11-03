from dash import dcc, html, Output, Input
from dash_bootstrap_components import Container, Tabs, Tab, Table

from dash_plotly.application import app
from vtb.position_report import PositionReport

url = '/position'  # Локальный адрес страницы

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

layout = Container([
    dcc.Upload(
        id='position-report-file',
        children=html.Div(['Перетащите или ', html.A('Выберите csv-файл')]),
        style=upload_style
    ),
    Tabs([
        Tab(label='Акции и Фонды', children=[html.Div(id='shares-report-table')]),
        Tab(label='Облигации', children=[html.Div(id='bonds-report-table')]),
    ]),
])


@app.callback(Output('shares-report-table', 'children'), Output('bonds-report-table', 'children'),
              Input('position-report-file', 'contents'))
def upload_position_report(contents):
    position_report = PositionReport()
    if contents is not None:
        position_report.save_to_db(contents)
    shares_table = Table.from_dataframe(position_report.get_shares_data(),
                                        striped=True, hover=True)
    bonds_table = Table.from_dataframe(position_report.get_bonds_data(),
                                       striped=True, hover=True)
    return shares_table, bonds_table
