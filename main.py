import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, dcc, Input, Output

from crime_data import df_race, arr_social

app = Dash(__name__, external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(id='race_graphic'),
        html.Div(
            'Choose minimum component of the black population in %'),
        dcc.Slider(id='black_range',
                   min=0,
                   max=100,
                   step=5,
                   value=0),

        html.Div(
            'Choose minimum component of the white population in %'),
        dcc.Slider(id='white_range',
                   min=0,
                   max=100,
                   step=5,
                   value=0),

        html.Div(
            'Choose minimum component of the asian population in %'),
        dcc.Slider(id='asian_range',
                   min=0,
                   max=100,
                   step=5,
                   value=0),

        html.Div(
            'Choose minimum component of the hispanic population in %'),
        dcc.Slider(id='hispanic_range',
                   min=0,
                   max=100,
                   step=5,
                   value=0),
    ]),

    html.Div(html.P([html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br()])
             ),

    html.Div([
        dcc.Graph(id='social_graphic'),
        html.Div(
            'Choose the severity of the murder'),
        dcc.Slider(id='murder_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=1),

        html.Div(
            'Choose the severity of the rape'),
        dcc.Slider(id='rape_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.7),

        html.Div(
            'Choose the severity of the robbery'),
        dcc.Slider(id='robbery_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.3),

        html.Div(
            'Choose the severity of the assault'),
        dcc.Slider(id='assault_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.5),

        html.Div(
            'Choose the severity of the burglary'),
        dcc.Slider(id='burglary_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.5),

        html.Div(
            'Choose the severity of the larceny'),
        dcc.Slider(id='larceny_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.2),

        html.Div(
            'Choose the severity of the auto theft'),
        dcc.Slider(id='theft_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.4),

        html.Div(
            'Choose the severity of the arson'),
        dcc.Slider(id='arson_severity',
                   min=0,
                   max=1,
                   step=0.1,
                   value=0.5),
    ])
])


@app.callback(
    Output('race_graphic', 'figure'),
    Input('black_range', 'value'),
    Input('white_range', 'value'),
    Input('asian_range', 'value'),
    Input('hispanic_range', 'value'))
def update_race_graph(pct_black,
                      pct_white,
                      pct_asian,
                      pct_hisp):
    df_race_filt = df_race
    df_race_filt = df_race_filt[df_race_filt['racepctblack'] >= pct_black]
    df_race_filt = df_race_filt[df_race_filt['racePctWhite'] >= pct_white]
    df_race_filt = df_race_filt[df_race_filt['racePctAsian'] >= pct_asian]
    df_race_filt = df_race_filt[df_race_filt['racePctHisp'] >= pct_hisp]

    df_race_filt = df_race_filt[['murders',
                                 'rapes',
                                 'robberies',
                                 'assaults',
                                 'burglaries',
                                 'larcenies',
                                 'autoThefts',
                                 'arsons']]

    df_race_filt = df_race_filt.sum(axis=0)
    fig = px.pie(df_race_filt,
                 values=df_race_filt.array,
                 names=df_race_filt.index)

    fig.update_layout(
        height=550,
        title_text='Distribution of crime patterns depending on racial composition',
        title_x=0.3)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


@app.callback(
    Output('social_graphic', 'figure'),
    Input('murder_severity', 'value'),
    Input('rape_severity', 'value'),
    Input('robbery_severity', 'value'),
    Input('assault_severity', 'value'),
    Input('burglary_severity', 'value'),
    Input('larceny_severity', 'value'),
    Input('theft_severity', 'value'),
    Input('arson_severity', 'value'))
def update_race_graph(murder_severity,
                      rape_severity,
                      robbery_severity,
                      assault_severity,
                      burglary_severity,
                      larceny_severity,
                      theft_severity,
                      arson_severity):
    arr_social_current = np.matmul(arr_social, [murder_severity,
                                                rape_severity,
                                                robbery_severity,
                                                assault_severity,
                                                burglary_severity,
                                                larceny_severity,
                                                theft_severity,
                                                arson_severity])

    sh_0, sh_1 = arr_social_current.shape
    x = np.linspace(0, 50, sh_1)
    y = np.linspace(0, 100, sh_0)

    fig = go.Figure(go.Surface(
        x=x,
        y=y,
        z=arr_social_current
    ))

    fig.update_layout(
        scene={
            'xaxis': {'nticks': 20},
            'zaxis': {'nticks': 4},
            'camera_eye': {'x': 0, 'y': -1, 'z': 0.5},
            'aspectratio': {'x': 1, 'y': 1, 'z': 0.2},
            'xaxis_title': 'affluence in %',
            'yaxis_title': 'born same state in %',
            'zaxis_title': 'criminality weight', })

    fig.update_layout(
        width=1400,
        height=750,
        title_text='Distribution of "criminality weight" (the severity of each crime can be choosen) '
                   'depending on local population percentage and affluence level',
        title_x=0.07)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
