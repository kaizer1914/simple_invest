from dash import Output, Input
from dash.dcc import Location
from dash_bootstrap_components import Container, NavbarSimple, NavItem, NavLink, Row

import all_bonds
from pages import all_shares, position
from pages.application import app

app.layout = Container([
    Location(id='url', refresh=False),
    Row(id='page-content')
])

navbar = NavbarSimple([
    NavItem(NavLink('Отчёт по позициям', href=position.url)),
    NavItem(NavLink('Акции', href=all_shares.url)),
    NavItem(NavLink('Облигации', href=all_bonds.url)),
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
    elif pathname == all_bonds.url:
        return navbar, all_bonds.layout
    else:
        return navbar


if __name__ == '__main__':
    app.run_server(debug=True)
