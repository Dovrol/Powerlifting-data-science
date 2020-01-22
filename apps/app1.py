import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from fetch_data import filtered_df, years, df
import plotly.graph_objs as go
from predicting import predict_total

from app import app


layout = html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H5('Equipped/Raw', className = 'text-center'),
                        dcc.Dropdown(id = 'eq',
                            options= [{'label':s, 'value':s} for s in filtered_df['Equipment'].unique()],
                            value='',
                            multi = True,
                        )
                    ]),
                    dbc.Col([
                        html.H5('Federation', className = 'text-center'),
                        dcc.Dropdown(id = 'fed',
                            options= [{'label':s, 'value':s} for s in filtered_df['Federation'].unique()],
                            value='',
                            multi = True,
                            # style = {'width': '70%'}
                        )  
                    ]),
                    dbc.Col([
                        html.H5('Event', className = 'text-center'),
                        dcc.Dropdown(id = 'event',
                            options= [{'label':s, 'value':s} for s in filtered_df['Event'].unique()],
                            value='',
                            multi = True,
                            # style = {'width': '70%'}
                        )  
                    ])
                ])
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id = 'loading',
                    children = ([ html.Div(id = 'output-graph1')]),
                    type = 'circle'
                    )
                ], className = 'display-1'),
            ], className = 'mx-5'),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.RadioItems(id = 'sex',
                        options= [
                            {'label':'  Male', 'value':'M'},
                            {'label': '  Female', 'value': 'F'}
                            ],
                        value='M',
                        labelStyle={'display': 'block'},
                        className = 'm-5'
                        )
                    ]),
                dbc.Col([
                    html.H5('Division', className = 'text-center'),
                        dcc.Dropdown(id = 'div',
                            options= [{'label':str(s), 'value':str(s)} for s in filtered_df['Division'].unique()],
                            value='',
                            multi = True,
                        )
                    ]) 
                ]),
            dbc.Row([
                dbc.Col([
                    dcc.Slider(
                    id='slider',
                    min=years.min(),
                    max=years.max(),
                    value=years.max(),
                    marks={str(year): str(year) for year in [x if x < years.max() else years.max() for x in range(int(years.min()), int(years.max()+4), 4)]},
                    step=1,
                    )
                    ])
                ], className = 'mb-5')
            ]),
            html.Div(className = 'border-top', style = {'margin-top': 150})
        ])

@app.callback(
    Output(component_id = 'output-graph1', component_property = 'children'),
    [Input(component_id = 'eq', component_property = 'value'),
    Input(component_id = 'fed', component_property = 'value'),
    Input(component_id = 'event', component_property = 'value'),
    Input(component_id = 'slider', component_property = 'value'),
    Input(component_id = 'sex', component_property = 'value'),
    Input(component_id = 'div', component_property = 'value')])
def update_graph(eq, fed, event, year, sex, div):
    global filtered_df
    data = filtered_df.copy()
    if eq:
        data = data.query(f'Equipment in {list(eq)}')
    if fed:
        data = data.query(f'Federation in {list(fed)}')
    if event:
        data = data.query(f'Event in {list(event)}')
    if year:
        data = data.query(f'Date < {year}')
    if sex:
        data = data.query(f'Sex in {list(sex)}')
    if div:
        data = data.query(f'Division in {list(div)}')

    predictions = predict_total(data)
    data = data.groupby(['WeightClassKg']).mean()['TotalKg'].sort_index()
    
    trace1 = go.Scatter(x = data.index, y = data.values,
                name = 'Mean total',
                )
    trace2 = go.Scatter(x = data.index, y = predictions,
                name = 'Predictions',
                )


    layout1 = go.Layout(
        title = 'Mean total for Bodyweight', 
        showlegend = True,
        xaxis = {'title': 'Bodyweight'},
        yaxis = {'title': 'Total in kg'},
        margin = {'l': 60, 'r': 60, 't': 100, 'b': 80})
    
    return dcc.Graph(
        id = 'graph1',
        figure = go.Figure(data = [trace1, trace2], layout = layout1)
        )

@app.callback(
    [Output(component_id = 'div', component_property = 'options'),
    Output(component_id = 'eq', component_property = 'options'),
    Output(component_id = 'event', component_property = 'options'),
    Output(component_id = 'fed', component_property = 'options')],
    [Input(component_id = 'fed', component_property = 'value'),
    Input(component_id = 'div', component_property = 'value'),
    Input(component_id = 'eq', component_property = 'value'),
    Input(component_id = 'event', component_property = 'value')])
def update_dropdown(fed, div, eq, event):
    global filtered_df
    data = filtered_df.copy()
    if eq:
        new_eq = [{'label':s, 'value':s} for s in data['Equipment'].unique()]
        data = data.query(f'Equipment in {list(eq)}')      
    else:
        new_eq = [{'label':s, 'value':s} for s in data['Equipment'].unique()]
    if fed:
        new_fed = [{'label':s, 'value':s} for s in data['Federation'].unique()]
        data = data.query(f'Federation in {list(fed)}')
    else:
        new_fed = [{'label':s, 'value':s} for s in data['Federation'].unique()]
    if event:
        new_event = [{'label':s, 'value':s} for s in data['Event'].unique()]
        data = data.query(f'Event in {list(event)}')
    else:
        new_event = [{'label':s, 'value':s} for s in data['Event'].unique()]
    if div:
        new_div = [{'label':str(s), 'value':str(s)} for s in data['Division'].unique()]
        data = data.query(f'Division in {list(div)}')
    else:
        new_div = [{'label':str(s), 'value':str(s)} for s in data['Division'].unique()]
    return new_div, new_eq, new_event, new_fed