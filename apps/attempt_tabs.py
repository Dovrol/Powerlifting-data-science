import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from fetch_data import filtered_df, years, df
import plotly.graph_objs as go
from predicting import predict_total

from app import app
from apps import attempt_selection


layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.P("How powerlifters increase their attempts",id = 'header', className = 'text-center my-5 display-4')
                ])
            ])
        ]),
        dcc.Tabs(id = 'tabs', children = [
            dcc.Tab(label = 'From first to second', children = [
                html.Div([
                    attempt_selection.attempt_layout_1_2
                ], className = 'mt-5')
        ]),
            dcc.Tab(label = 'From second to third', children = [
                html.Div([
                    attempt_selection.attempt_layout_2_3
                ], className = 'mt-5')
            ])
        ])
    ])