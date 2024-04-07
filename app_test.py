import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

# Define your layout
app.layout = html.Div(style={'width': '80%', 'margin': 'auto'}, children=[
    html.H1('My Dash App'),
    
    html.Div(style={'display': 'flex'}, children=[
        dcc.Graph(
            id='graph1',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Bar chart'},
                ],
                'layout': {
                    'title': 'Bar chart'
                }
            },
            style={'width': '50%'}
        ),
        
        dcc.Graph(
            id='graph2',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': 'Line chart'},
                ],
                'layout': {
                    'title': 'Line chart'
                }
            },
            style={'width': '50%'}
        )
    ]),
    html.Div(style={'display': 'flex'}, children = [
        html.H2('Hallo dit is een testbericht')])
])

if __name__ == '__main__':
    app.run_server(debug=True)
