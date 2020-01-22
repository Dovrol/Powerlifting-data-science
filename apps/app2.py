import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from fetch_data import filtered_df, years, df
import plotly.graph_objs as go
import dash_table
from app import app
import pandas as pd


layout = html.Div([
            dbc.Container([
                html.H1('Individual Analyst', className = 'display-4 my-5 text-center'),
                html.Div([
                    html.Label('Powerlifter Name: '),
                    dbc.Input(id = 'input2', value = 'Taylor Atwood', type = 'text', style = {'width': '20%'}), 
                ]),
            ]),
            dcc.Loading([
                html.Div([html.Div(id = 'output-graph2')],className = 'mx-5'),
                dbc.Container([
                    dash_table.DataTable(
                        id = 'table', 
                        columns = [{'name': i, 'id': i} for  i in filtered_df.columns],
                        data = filtered_df.copy()[df['Name'] == 'Taylor Atwood'].to_dict('records'),
                        # css = [{"selector": ".dash-spreadsheet", "rule": 'font-family: "monospace"'}]
                        style_table={'overflowX': 'scroll',
                            'maxHeight': '400px',
                            'overflowY': 'scroll',
                            'border': 'thin lightgrey solid'},
                        style_as_list_view=True,
                        style_cell={'padding': '5px'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[{
                            "if": {"column_id": 'TotalKg'},
                            "backgroundColor": "#3D9970",
                            'color': 'white'
                        }]
                    )
                ], className = 'mb-5') 
            ])
        ])




@app.callback(
    Output(component_id = 'table', component_property = 'data'),
    [Input(component_id = 'input2', component_property = 'value')])
def update_lifter(lifter):
    global filtered_df
    competitor = filtered_df.copy()[df['Name'] == lifter]
    return competitor.to_dict('records')

@app.callback(
    Output(component_id = 'output-graph2', component_property = 'children'),
    [Input(component_id = 'input2', component_property = 'value')])
def plot_progress(name):
    global filtered_df
    competitor = filtered_df.copy()[df['Name'] == name]
    if competitor.empty:
        return html.H2("Sorry we don't have such a lifter in our database.", className = 'text-center m-5')
    # competitor = competitor[competitor['Federation'] == 'IPF']
    competitor['Date'] = pd.to_datetime(competitor['Date'])
    competitor.set_index('Date', inplace = True)
#     competitor.sort_values(by = 'Date')
    
    for total in competitor['TotalKg']:
        if total + 200 < competitor['TotalKg'].mean():
            competitor[competitor['TotalKg'] == total] = None
            
    competitor['TotalKg'].dropna(inplace = True)
    data = competitor['TotalKg'].sort_index()

    total = go.Scatter(x = data.index, y = data.values,
                name = 'Total'
                )
    layout1 = go.Layout(title = f'{name} total in Kg', showlegend = True)


    return dcc.Graph(
        id = 'graph2',
        figure = go.Figure(data = [total], layout = layout1)
        )
