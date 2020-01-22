import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from fetch_data import filtered_df, years, df
import plotly.graph_objs as go
from predicting import predict_total

from app import app
from apps import app1, app3_general_date


layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.P("General statistics for powerlifting",id = 'header', className = 'text-center my-5 display-4')
                ])
            ])
        ]),
        dcc.Tabs(id = 'tabs', children = [
            dcc.Tab(label = 'Total by bodyweight', children = [
                html.Div([
                    app1.layout
                ], className = 'mt-5')
        ]),
            dcc.Tab(label = 'Total by date', children = [
                html.Div([
                    app3_general_date.layout
                ], className = 'mt-5')
            ])
        ])
    ])