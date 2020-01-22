import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from fetch_data import filtered_df, years, df
import plotly.graph_objs as go
from predicting import predict_total
import numpy as np

from app import app

layout = html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H5('Equipped/Raw', className = 'text-center'),
                        dcc.Dropdown(id = 'eq2',
                            options= [{'label':s, 'value':s} for s in filtered_df['Equipment'].unique()],
                            value='',
                            multi = True,
                        )
                    ]),
                    dbc.Col([
                        html.H5('Federation', className = 'text-center'),
                        dcc.Dropdown(id = 'fed2',
                            options= [{'label':s, 'value':s} for s in filtered_df['Federation'].unique()],
                            value='',
                            multi = True,
                            # style = {'width': '70%'}
                        )  
                    ]),
                    dbc.Col([
                        html.H5('Event', className = 'text-center'),
                        dcc.Dropdown(id = 'event2',
                            options= [{'label':s, 'value':s} for s in filtered_df['Event'].unique()],
                            value='',
                            multi = True,
                            # style = {'width': '70%'}
                        )  
                    ]),
                    dbc.Col([
                        html.H5('Weight Class (Kg)', className = 'text-center'),
                        dcc.Dropdown(id = 'weight',
                            options= [{'label':str(round(float(s), 1)), 'value':s} if s != '120+' else {'label':s, 'value':s} for s in np.unique(([s if s < 120 else '120+' for s in filtered_df['WeightClassKg'].unique()]))],
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
                    children = ([ html.Div(id = 'output-graph3')]),
                    type = 'circle'
                    )
                ], className = 'display-1'),
            ], className = 'mx-5'),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.RadioItems(id = 'sex2',
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
                        dcc.Dropdown(id = 'div2',
                            options= [{'label':str(s), 'value':str(s)} for s in filtered_df['Division'].unique()],
                            value='',
                            multi = True,
                        )
                    ]) 
                ])
            ]),
            html.Div(className = 'border-top', style = {'margin-top': 150})
        ])

@app.callback(
    Output(component_id = 'output-graph3', component_property = 'children'),
    [Input(component_id = 'eq2', component_property = 'value'),
    Input(component_id = 'fed2', component_property = 'value'),
    Input(component_id = 'event2', component_property = 'value'),
    Input(component_id = 'sex2', component_property = 'value'),
    Input(component_id = 'div2', component_property = 'value'),
    Input(component_id = 'weight', component_property = 'value')])
def update_graph(eq, fed, event, sex, div, weights):
    global filtered_df
    data = filtered_df.copy()
    if eq:
        data = data.query(f'Equipment in {list(eq)}')
    if fed:
        data = data.query(f'Federation in {list(fed)}')
    if event:
        data = data.query(f'Event in {list(event)}')
    if sex:
        data = data.query(f'Sex in {list(sex)}')
    if div:
        data = data.query(f'Division in {list(div)}')
    if weights:
        traces = []
        for weight in weights:
            if weight == '120+':
                    class_ = data[data['WeightClassKg'] > 120]
            else:
                class_ = data[data['WeightClassKg'] == float(weight)]
            class_['Date'] = class_['Date'].map(lambda x: x.year)
            class_ = class_[class_['Date'] > 2010]
            final = class_.groupby('Date').mean()['TotalKg']
            trace = go.Scatter(x = final.index, y = final.values, name = weight)
            traces.append(trace)

        # predictions = predict_total(data)
        data = data.groupby(['WeightClassKg']).mean()['TotalKg'].sort_index()
        

        layout1 = go.Layout(
            title = 'Mean total in each year', 
            showlegend = True,
            xaxis = {'title': 'Year'},
            yaxis = {'title': 'Total (KG)'},
            margin = {'l': 60, 'r': 60, 't': 100, 'b': 80})
        
        return dcc.Graph(
            id = 'graph1',
            figure = go.Figure(data = traces, layout = layout1)
            )

    else:
        return dbc.Container([
            html.H1('Please choose a weight class')
        ], className = 'my-5 text-center')

@app.callback(
    [Output(component_id = 'div2', component_property = 'options'),
    Output(component_id = 'eq2', component_property = 'options'),
    Output(component_id = 'event2', component_property = 'options'),
    Output(component_id = 'fed2', component_property = 'options')],
    [Input(component_id = 'fed2', component_property = 'value'),
    Input(component_id = 'div2', component_property = 'value'),
    Input(component_id = 'eq2', component_property = 'value'),
    Input(component_id = 'event2', component_property = 'value')])
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

