import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem('General statistics', href="/general"),
                dbc.DropdownMenuItem('Individual statistics', href="/individual"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Home page", href="/"),
            ],
        ),
    ],
    brand="Lifting academy",
    brand_href="/",
    sticky = 'top'
)
headline = dbc.Container(
    [
        html.Div([
            html.P("Explore Powerlifting with Data Analyst", className="display-4"),
            html.Hr(className="my-2"),
            html.P('Source of the lifting knowladge', className = 'lead font-weight-normal')
            
        ], className = "col-md-5 p-md-5 mx-auto")
    ], className = 'p-xl-5 mx-xl-3 text-center bg-light', style = {'height': '50vh'}, fluid = True
)

# content = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.H2('General statistics', className = 'text-center text-light'),
#             html.Div([
#                 dcc.Link('Analize !', href="/general", className = 'btn btn-primary')
#             ], style = {'text-align': 'center'}, className = 'mt-5')
#         ], className = 'bg-dark col-5 p-5 rounded-lg border border-light mr-1'),
#         dbc.Col([
#             html.H2('Individual statistics', className = 'text-center'),
#             html.Div([
#                 dcc.Link('Analize !', href="/individual", className = 'btn btn-primary')
#             ], style = {'text-align': 'center'}, className = 'mt-5')
#         ], className = 'col-5 p-5 rounded-lg border border-dark ml-1 ', style = {'width': 500, 'height': 300})
#     ], className ='justify-content-center mt-4')
# ], className ='justify-content-center', fluid = True)

content = html.Div([
        html.Div([
            html.H2('General statistics', className = 'text-center text-light'),
            html.Div([
                dcc.Link('Analize !', href="/general", className = 'btn btn-primary')
                    ], style = {'text-align': 'center'}, className = 'mt-5')
                ], className = 'col-6 bg-dark py-5', style = {'height': '50vh'}),
        html.Div([
            html.H2('Individual statistics', className = 'text-center'),
            html.Div([
                dcc.Link('Analize !', href="/general", className = 'btn btn-primary')
                    ], style = {'text-align': 'center'}, className = 'mt-5')
                ], className = 'col-6 my-5', style = {'height': '50vh'})
            ], className = 'row')

footer = dbc.Jumbotron([
    dbc.Row([
        dbc.Col([
        ], className = 'col-12')
    ])
], fluid = True)