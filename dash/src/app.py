import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import os
import requests

app = dash.Dash(__name__)
server = app.server
df_1 = pd.DataFrame.from_records(requests.get("http://api:5000/getHand", params={'limit': 10}).json()["data"])
print(df_1)
df_2=pd.DataFrame.from_records(requests.get("http://api:5000/getMinutesMatch", params={'limit': 10}).json()["data"])
print(df_2)
df_3 = pd.DataFrame.from_records(requests.get("http://api:5000/getTitles", params={'limit': 10}).json()["data"])
print(df_3)
df_4 = pd.DataFrame.from_records(requests.get("http://api:5000/getAgeWinners", params={'limit': 10}).json()["data"])
df_4.rename(columns = {'round':'age'}, inplace = True)
print(df_4)
df_5 = pd.DataFrame.from_records(requests.get("http://api:5000/getLevel", params={'limit': 10}).json()["data"])
print(df_5)
df_6 = pd.DataFrame.from_records(requests.get("http://api:5000/getQuantityByCountry", params={'limit': 10}).json()["data"])
print(df_6)
df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6], axis=1)
print(df.head())

print(os.listdir())
app.layout = html.Div([
    html.Div([
        html.H2(['Analysis of tennis players']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                {'label': 'Player titles', 'value': 'titles'},
                {'label': 'Player hand', 'value': 'hand'},
                {'label': 'Сountry', 'value': 'country_id'},
                {'label': 'Winners age', 'value': 'age'},
                {'label': 'Match time', 'value': 'minutes'},
                {'label': 'Player level', 'value': 'level'}
            ],
            multi=False,
            clearable=False,
            style={"width": "50%"}

        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])


# ---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(my_dropdown):
    dff = df

    return px.pie(data_frame=dff, names=my_dropdown, hole=0.3, )




