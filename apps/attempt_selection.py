import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from fetch_data import filtered_df, years, df
import plotly.graph_objs as go
import dash_table
from app import app
import pandas as pd

attempts = df[['Squat1Kg', 'Squat2Kg', 'Squat3Kg', 'Bench1Kg', 'Bench2Kg', 'Bench3Kg', 'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg']].dropna(axis = 0)
squat = attempts[['Squat1Kg', 'Squat2Kg', 'Squat3Kg']]
bench = attempts[['Bench1Kg', 'Bench2Kg', 'Bench3Kg']]
deadlift = attempts[['Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg']]
squat['1-2'] = None
squat['2-3'] = None

bench['1-2'] = None
bench['2-3'] = None

deadlift['1-2'] = None
deadlift['2-3'] = None

squat['1-2'] = round(abs(squat['Squat2Kg'])*100/abs(squat['Squat1Kg']) - 100)
squat['2-3'] = round(abs(squat['Squat3Kg'])*100/abs(squat['Squat2Kg']) - 100)

bench['1-2'] = round(abs(bench['Bench2Kg'])*100/abs(bench['Bench1Kg']) - 100)
bench['2-3'] = round(abs(bench['Bench3Kg'])*100/abs(bench['Bench2Kg']) - 100)

deadlift['1-2'] = round(abs(deadlift['Deadlift2Kg'])*100/abs(deadlift['Deadlift1Kg']) - 100)
deadlift['2-3'] = round(abs(deadlift['Deadlift3Kg'])*100/abs(deadlift['Deadlift2Kg']) - 100)

squat_12 = squat['1-2'].value_counts()[squat['1-2'].value_counts().values > 10]
bench_12 = bench['1-2'].value_counts()[bench['1-2'].value_counts().values > 10]
deadlift_12 = deadlift['1-2'].value_counts()[deadlift['1-2'].value_counts().values > 10]

squat_23 = squat['2-3'].value_counts()[squat['2-3'].value_counts().values > 10]
bench_23 = bench['2-3'].value_counts()[bench['2-3'].value_counts().values > 10]
deadlift_23 = deadlift['2-3'].value_counts()[deadlift['2-3'].value_counts().values > 10]

s12 = go.Bar(x = squat_12.index, y = squat_12.values, name = 'Squat 1-2')
b12 = go.Bar(x = bench_12.index, y = bench_12.values, name = 'Bench 1-2')
d12 = go.Bar(x = deadlift_12.index, y = deadlift_12.values, name = 'Deadlift 1-2')

s23 = go.Bar(x = squat_23.index, y = squat_23.values, name = 'Squat 2-3')
b23 = go.Bar(x = bench_23.index, y = bench_23.values, name = 'Bench 2-3')
d23 = go.Bar(x = deadlift_23.index, y = deadlift_23.values, name = 'Deadlift 2-3')

layout_1_2 = go.Layout(title = 'Graph', xaxis ={'range': [1, 20], 'title': 'Incresed second attempt of each lift (in %)'},
                  yaxis = {'title':'Population'})
attempts_12 = go.Figure(data = [s12, b12, d12], layout = layout_1_2)


attempt_layout_1_2 = html.Div([
            dcc.Loading([
                html.Div([html.Div([
                    dcc.Graph(
                            figure = attempts_12
                            )], id = 'attempt-output')],className = 'mx-5'),
                    ])
                ])
layout_2_3 = go.Layout(title = 'Graph', xaxis ={'range': [1, 20], 'title': 'Incresed third attempt of each lift (in %)'},
                  yaxis = {'title':'Population'})                
attempts_23 = go.Figure(data = [s23, b23, d23], layout = layout_2_3)
attempt_layout_2_3 = html.Div([
            dcc.Loading([
                html.Div([html.Div([
                    dcc.Graph(
                            figure = attempts_23
                            )], id = 'attempt-output')],className = 'mx-5'),
                    ])
                ])


