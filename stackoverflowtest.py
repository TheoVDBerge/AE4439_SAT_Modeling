from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Iris bar figure
def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Data
df = px.data.iris()

# Build App
app = Dash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure() 
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure() 
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure()
                ], width=9),
                dbc.Col([
                    drawFigure()
                ], width=3),
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
app.run_server()