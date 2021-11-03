from dash import html, Output, Input
from dash.dcc import Location, Link
from dash_bootstrap_components import Container

from dash_plotly import all_shares, position
from dash_plotly.application import app

app.layout = Container([
    Location(id='url', refresh=False),
    html.Div(id='page-content')
])

menu_layout = html.Div([
    Link('Отчёт по позициям', href=position.url),
    html.Br(),
    Link('Список акций Московской биржи', href=all_shares.url),
    html.Br(),
])


@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == position.url:
        return position.layout
    elif pathname == all_shares.url:
        return all_shares.layout
    else:
        return menu_layout


if __name__ == '__main__':
    app.run_server(debug=True)
