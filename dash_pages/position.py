import pandas
import plotly.express as px
from dash import dcc, html, Output, Input
from dash.dcc import Graph
from dash_bootstrap_components import Tabs, Tab, Row, Table, Alert, Col

from dash_pages.application import app
from vtb.position_report import PositionReport

url = '/position'  # Локальный адрес страницы

upload_id = 'position-report-file'
shares_tab_id = 'shares-tab-report'
bonds_tab_id = 'bonds-tab-report'
total_tab_id = 'total-tab-report'

upload_style = {
    'width': '100%',
    'height': '100px',
    'lineHeight': '100px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'marginBottom': '20px',
    'marginTop': '20px',
}

ticker_label = 'Тикер'
name_label = 'Наименование'
count_label = 'Количество, шт.'
buy_sum_label = 'Сумма приобретения, ₽'
change_sum_label = 'Изменение суммы, ₽'
current_sum_label = 'Текущая сумма, ₽'
income_label = 'Прибыль, %'
weight_label = 'Доля, %'
sectype_label = 'Тип'
couponperiod_label = 'Период купона, дн.'
couponpercent_label = 'Процент купона, %'
effectiveyield_label = 'Эффективная доходность, %'
duration_label = 'Дюрация, дн.'
enddate_label = 'Дата погашения'

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


def add_shares_weight_graph(shares_df) -> Graph:
    df = shares_df[['name', 'ticker', 'current_sum']]
    pie_fig = px.pie(df, values='current_sum', names='name', hover_data=['ticker'],
                     labels={
                         'ticker': ticker_label,
                         'name': name_label,
                         'current_sum': current_sum_label,
                     },
                     title='По долям',
                     template='plotly_dark')
    pie_graph = Graph(figure=pie_fig, style={'marginTop': '20px'})
    return pie_graph


def add_shares_sum_graph(shares_df) -> Graph:
    df = shares_df[['name', 'ticker', 'current_sum', 'change_sum']]
    bar_fig = px.bar(df, x='ticker', y='current_sum', color='change_sum', hover_data=['name'],
                     labels={
                         'ticker': ticker_label,
                         'name': name_label,
                         'current_sum': current_sum_label,
                         'change_sum': change_sum_label,
                     },
                     title='По сумме',
                     template='plotly_dark')
    bar_graph = Graph(figure=bar_fig, style={'marginTop': '20px'})
    return bar_graph


def add_shares_income_graph(shares_df) -> Graph:
    shares_income_df = shares_df[['name', 'ticker', 'change_sum', 'current_sum']]
    bar_fig = px.bar(shares_income_df, x='ticker', y='change_sum',
                     # color='change_sum',
                     hover_data=['name', 'current_sum'],
                     labels={
                         'ticker': ticker_label,
                         'name': name_label,
                         'current_sum': current_sum_label,
                         'change_sum': change_sum_label,
                     },
                     title='По доходности',
                     template='plotly_dark')
    bar_graph = Graph(figure=bar_fig, style={'marginTop': '20px'})
    return bar_graph


def add_shares_table(shares_df) -> Col:
    shares_df = shares_df[['ticker', 'name', 'count', 'buy_sum', 'change_sum', 'current_sum', 'income', 'weight']]
    shares_table = Table.from_dataframe(shares_df, striped=True, hover=True,
                                        header={
                                            'ticker': ticker_label,
                                            'name': name_label,
                                            'count': count_label,
                                            'buy_sum': buy_sum_label,
                                            'change_sum': change_sum_label,
                                            'current_sum': current_sum_label,
                                            'income': income_label,
                                            'weight': weight_label,
                                        })
    return Col([shares_table], style={'marginTop': '20px'})


def add_bonds_table(bonds_df) -> Col:
    bonds_table_df = bonds_df[
        ['name', 'couponperiod', 'couponpercent', 'effectiveyield', 'duration', 'enddate', 'count', 'current_sum']]
    bonds_table = Table.from_dataframe(bonds_table_df, striped=True, hover=True,
                                       header={
                                           'name': name_label,
                                           'couponperiod': couponperiod_label,
                                           'couponpercent': couponpercent_label,
                                           'effectiveyield': effectiveyield_label,
                                           'duration': duration_label,
                                           'enddate': enddate_label,
                                           'count': count_label,
                                           'current_sum': current_sum_label,
                                       })
    return Col([bonds_table], style={'marginTop': '20px'})


def add_bonds_corp_graph(bonds_df) -> Graph:
    bonds_company_df = bonds_df[['name', 'current_sum', 'sectype']]
    company = lambda longname: longname.rsplit(' ', 1)[0]

    bonds_corp_df = bonds_company_df[bonds_company_df['sectype'].isin(['Корпоративные'])]
    bonds_corp_df['company'] = bonds_corp_df['name'].apply(company)
    bonds_corp_df.groupby('name').sum()

    pie_corp_fig = px.pie(bonds_corp_df, values='current_sum', names='company',
                          labels={'current_sum': current_sum_label, 'company': 'Компания'},
                          title='Корпоративные', template='plotly_dark')
    pie_corp_graph = Graph(figure=pie_corp_fig, style={'marginTop': '20px'})
    pie_corp_fig.update_traces(textinfo='none')
    return pie_corp_graph


def add_bonds_region_graph(bonds_df) -> Graph:
    bonds_company_df = bonds_df[['name', 'current_sum', 'sectype']]
    region = lambda longname: longname.rsplit(' ', 1)[0]

    bonds_region_df = bonds_company_df[bonds_company_df['sectype'].isin(['Муниципальные'])]
    bonds_region_df['region'] = bonds_region_df['name'].apply(region)
    bonds_region_df.groupby('name').sum()

    pie_region_fig = px.pie(bonds_region_df, values='current_sum', names='region',
                            labels={'current_sum': current_sum_label, 'region': 'Регион'},
                            title='Муниципальные', template='plotly_dark')
    pie_region_graph = Graph(figure=pie_region_fig, style={'marginTop': '20px'})
    return pie_region_graph


def add_bonds_ofz_graph(bonds_df) -> Graph:
    bonds_company_df = bonds_df[['name', 'current_sum', 'sectype']]
    ofz = lambda longname: longname.split(' ', 1)[0]

    bonds_ofz_df = bonds_company_df[bonds_company_df['sectype'].isin(['ОФЗ'])]
    bonds_ofz_df['type'] = bonds_ofz_df['name'].apply(ofz)
    bonds_ofz_df.groupby('name').sum()

    pie_ofz_fig = px.pie(bonds_ofz_df, values='current_sum', names='type',
                         labels={'current_sum': current_sum_label, 'type': 'Тип'},
                         title='Государственные', template='plotly_dark')
    pie_ofz_graph = Graph(figure=pie_ofz_fig, style={'marginTop': '20px'})
    return pie_ofz_graph


def add_bonds_type_graph(bonds_df, bonds_etf_df) -> Graph:
    bonds_sectype_df = bonds_df[['sectype', 'current_sum']]
    bonds_etf_df = bonds_etf_df[['sectype', 'current_sum']]
    bonds_sectype_df = pandas.concat([bonds_sectype_df, bonds_etf_df])

    pie_fig = px.pie(bonds_sectype_df, values='current_sum', names='sectype',
                     labels={
                         'current_sum': current_sum_label,
                         'sectype': sectype_label,
                     },
                     title='По типу',
                     template='plotly_dark')
    pie_graph = Graph(figure=pie_fig, style={'marginTop': '20px'})
    return pie_graph


def add_total_graph(total_df) -> Graph:
    pie_fig = px.pie(total_df, values='sum', names='assets',
                     labels={'assets': 'Активы', 'sum': 'Сумма'},
                     title='Активы',
                     template='plotly_dark')
    pie_graph = Graph(figure=pie_fig, style={'marginTop': '20px'})
    return pie_graph


@app.callback(Output(total_tab_id, 'children'), Output(shares_tab_id, 'children'), Output(bonds_tab_id, 'children'),
              Input(upload_id, 'contents'))
def upload_position_report(contents):
    if contents is None:
        alert = Alert(['Нет данных'], color='dark', style={'marginTop': '20px'})
        return alert, alert, alert
    elif contents is not None:
        position_report = PositionReport(contents)

        shares_report = Row([
            add_shares_weight_graph(position_report.shares_df),
            add_shares_sum_graph(position_report.shares_df),
            add_shares_income_graph(position_report.shares_df),
            add_shares_table(position_report.shares_df),
        ])
        bonds_report = Row([
            add_bonds_type_graph(position_report.bonds_df, position_report.bonds_etf_df),
            add_bonds_corp_graph(position_report.bonds_df),
            add_bonds_region_graph(position_report.bonds_df),
            add_bonds_ofz_graph(position_report.bonds_df),
            add_bonds_table(position_report.bonds_df),
        ])
        total_report = Row([
            add_total_graph(position_report.total_df),
        ])
        return total_report, shares_report, bonds_report
