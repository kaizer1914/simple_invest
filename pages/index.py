from dash import Output, Input
from dash.dcc import Location
from dash_bootstrap_components import Container, NavbarSimple, NavItem, NavLink, Row

from pages import all_shares, position
from pages.application import app

app.layout = Container([
    Location(id='url', refresh=False),
    Row(id='page-content')
])

navbar = NavbarSimple([
    NavItem(NavLink('Отчёт по позициям', href=position.url)),
    NavItem(NavLink('Акции Мосбиржи', href=all_shares.url)),
],
    brand='Инвест',
    color='primary',
    dark=True,
    style={'marginBottom': '20px'})


@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == position.url:
        return navbar, position.layout
    elif pathname == all_shares.url:
        return navbar, all_shares.layout
    else:
        return navbar


if __name__ == '__main__':
    app.run_server(debug=True)
