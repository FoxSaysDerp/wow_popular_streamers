import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import requests

# twitch api login
client_id = 'X'
headers = {'Client-ID': client_id}
games_url = 'https://api.twitch.tv/helix/games'
streams_url = 'https://api.twitch.tv/helix/streams'

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundImage': 'linear-gradient(to right top, #30293d, #392e4f, #433362, #4c3775, #563c89, #5f4296, #6848a3, #714eb0, #7a58b9, #8461c2, #8d6bcb, #9775d4)', 'padding': 30}, children=[
    html.H1(
        children='Najwięksi streamerzy z gry World of Warcraft',
        style={'textAlign': 'center', 'fontWeight': 900, 'fontStyle': 'bold', 'color': '#341e63'}
    ),

    html.Div(
        children='Streamerzy z największą ilością widzów na platformie Twitch',
        style={'textAlign': 'center', 'fontSize': 40, 'color': '#341e63'}
    ),

    html.Label('Gra', style={'textAlign': 'center', 'fontSize': 40, 'color': '#341e63', 'visibility': 'hidden'}),
    dcc.Input(id='game_name', value='World of Warcraft', style={'visibility': 'hidden'}),

    html.Label('Ilość streamów', style={'textAlign': 'center', 'fontSize': 40, 'color': '#341e63', 'marginTop': 30}),
    dcc.Slider(
        id='stream_num',
        min=5,
        max=50,
        marks={i * 5: str(i * 5) for i in range(1, 11)},
        value=10,
    ),

    dcc.Graph(id='jobs_barchart', style={'marginTop': 30, 'marginBottom': 30}),

    html.Button(id='submit-button', n_clicks=0, children='Odśwież',
                style={
                    'display': 'block',
                    'margin': 'auto',
                    'width': 200,
                    'textAlign': 'center',
                    'fontSize': 15,
                    'fontFamily': 'inherit',
                    'color': '#d5cce8',
                    'border-color': '#d5cce8',
                    'border-width': 2,
                }
                ),
])


@app.callback(
    Output(component_id='jobs_barchart', component_property='figure'),
    [Input(component_id='submit-button', component_property='n_clicks'), ],
    [State(component_id='game_name', component_property='value'),
     State(component_id='stream_num', component_property='value'), ],
)
def update_figure(n_clicks, game, n_streams):
    if game == '':
        payload = {'first': n_streams}
        r = requests.get(streams_url, headers=headers, params=payload).json()
    else:
        payload = {'name': game}
        r = requests.get(games_url, headers=headers, params=payload).json()
        game_id = r['data'][0]['id']
        payload = {'game_id': game_id, 'first': n_streams}
        r = requests.get(streams_url, headers=headers, params=payload).json()

    return {
        'data': [
            go.Bar(
                x=[d['user_name']],
                y=[d['viewer_count']],
                text=d['title'],
                name=d['user_name'],
                hoverinfo='x+y+text',
                showlegend=False
            ) for d in r['data']
        ],
        'layout': go.Layout(
            xaxis={'title': 'Streamerzy'},
            yaxis={'title': 'Ilość widzów'},
            hovermode='closest',
            title=game + ' - streamerzy z największą ilością widzów',
            # font=dict(family='OpenSansCondensed, Arial, Helvetica, sans serif'),
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
