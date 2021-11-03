import dash_bootstrap_components
from dash import Dash

app = Dash('invest', suppress_callback_exceptions=True,
           external_stylesheets=[dash_bootstrap_components.themes.SOLAR])
flast_server = app.server  # Доступ к серверу Flask
