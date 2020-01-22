import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import app1, app2, home_page, general_tabs, attempt_tabs



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/general':
        return home_page.navbar, general_tabs.layout, attempt_tabs.layout
    elif pathname == '/individual':
        return home_page.navbar, app2.layout
    else:
        return home_page.headline, home_page.content

if __name__ == '__main__':
    app.run_server(debug=True)