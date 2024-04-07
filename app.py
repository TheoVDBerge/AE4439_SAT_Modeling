# Import required libraries
import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table as dt
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input
from dash.dependencies import Output
import dash_bootstrap_components as dbc
from main_data import df
print('Imported main_data.py')
from airport_data import df_airport
print('Imported airport data')
from helper_functions import getFlightRoutes 
print('Imported helper_functions.py')
#%%
print('Imported all requirements')

flight_routes = getFlightRoutes(df)

print('Initialised flight routes')

# Initialize the app
app = Dash(__name__)
# app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
# app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
# app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = 'SAT modeling project'

print('Initialised the web-app')

"""
To do:
    - Filter opties maken
    - Functies maken om data te filteren
    - Flight routes filteren in functie maken en dan helper_functions.py maken
    - ?
"""


# TODO: Fix the route column breaking the code
df2 = df.drop(columns=['route'])



# Map of airports and routes
def getmap(id_, flight_routes):
    fig = go.Figure(go.Scattergeo())
        
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_airport['lon'],
        lat = df_airport['lat'],
        hoverinfo = 'text',
        text = df_airport["iata"] + ' - ' + df_airport['name'],
        mode = 'markers',
        marker = dict(
            size = 5,
            color = 'rgb(255, 0, 0)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))
    max_ = 0
    for i in flight_routes:
        max_ = i[-1] if i[-1] > max_ else max_
        
    for routes in flight_routes:
        for leg in routes[0]:
            fig.add_trace(
                go.Scattergeo(
                    locationmode = 'USA-states',
                    lon = [(df_airport[df_airport['iata'] == leg[0]])['lon'].iloc[0], (df_airport[df_airport['iata'] == leg[1]])['lon'].iloc[0]],
                    lat = [(df_airport[df_airport['iata'] == leg[0]])['lat'].iloc[0], (df_airport[df_airport['iata'] == leg[1]])['lat'].iloc[0]],
                    mode = 'lines',
                    line = dict(width = 1,color = 'red'),
                    opacity = float(routes[1])/max_,
                    hoverinfo = 'skip',
                    text = f'{leg[0]} - {leg[1]}',
                        ))


    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=20),
        title_text = 'Legs for selected data (hover for airport names)',
        title_x = 0.5,
        showlegend = False,
        geo = dict(
            scope = 'world',
            projection_type = 'natural earth',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
            framecolor = 'black'
            #bgcolor='#272b30',
        ),
        template = 'plotly_dark'
        # plot_bgcolor='black',
        # paper_bgcolor='black'
        # width = 1000,
        # height = 600
    )
    return (html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(id = id_,
                          figure = fig)
            ])
        )
    ]), fig)




def drawDropdownWithoutCard(options_, id_, placeholder_, width_):
    # Options must be a list
    return(dcc.Dropdown(
                    id = id_,
                    options = options_,
                    placeholder = placeholder_,
                    multi = True,
                    style = {'width': width_})                  
                    
        )


def drawDropdown(options_, id_, placeholder_, width_):
    # Options must be a list
    return(html.Div([
        dbc.Card(
            dbc.CardBody([
                drawDropdownWithoutCard(options_, id_, placeholder_, width_),
                    
                    ]),
            )])
        )

# def drawDropdown(options_, id_, placeholder_, width_):
#     # Options must be a list
#     return(html.Div([
#         dbc.Card(
#             dbc.CardBody([
#                 dcc.Dropdown(
#                     id = id_,
#                     options = options_,
#                     placeholder = placeholder_,
#                     multi = True,
#                     style = {'width': width_}),
                    
#                     ]),
#             )])
#         )


def drawTable(data_, id_):
    table = dt.DataTable(
        id = id_,
        columns=[{"name": i, "id": i} for i in data_.columns],
        data = data_.to_dict("records"),
        page_size = 50
        )
    table.className='table-dark'
    return(html.Div([
        dbc.Card(
            dbc.CardBody([
                table                
                ])
            )
        ])
        
        )

def drawDonutChart(data_, id_, title_):
    fig = go.Figure(
        data = go.Pie(
            labels = list(df.dest.unique()),
            values = [(df[df.dest.isin([x])]['totalWeight'].sum()/1000) for x in list(df.dest.unique())],
            hole = 0.4,
            textinfo = 'label+percent',
            insidetextorientation = 'radial'))
    fig.update_layout(
        annotations=[dict(text=f'  Total: <br> {df.totalWeight.sum()/1000}', x=0.5, y=0.5, font_size=15, showarrow=False, align = 'center')],
       title={'text': title_, 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
       template = 'plotly_dark'
   )
    return(html.Div([
        dbc.Card(
            dbc.CardBody([dcc.Graph(id = id_,
                      figure = fig)
                ])
            
            )
        ])
        ,fig)

def drawRangeSliderWithoutCard(data_, id_):       
    return(dcc.RangeSlider(0, 24, 0.5,
        marks = {k: {'label': f'{k}:00',
                     'style': {'transform':'rotate(45deg)'}} for k in range(0,25)},
        value=[5, 15], id=id_, allowCross = False))

def drawRangeSlider(data_, id_):
    return(html.Div([
        dbc.Card(
            dbc.CardBody([
                 drawRangeSliderWithoutCard(data_, id_) 
                ])
            )
        ])
        )

# Main website lay-out
# app.layout = html.Div(style={'width':'80%', 'margin':'auto'}, children=[
app.layout = html.Div(children=[
    dbc.Card(
        dbc.CardBody([
            # Header text
            dbc.Row([
                dbc.Col([
                    html.H2('AE4439 SAT Modelling project', className='text-center')
                ])
            ]),

            # First row, map and filter options
            dbc.Row([
                # Map
                dbc.Col([
                    getmap('map', flight_routes)[0]
                ], width=7),
                # Filter options
                # dbc.Col([
                #     dbc.Col([
                #         html.H6('Flight number'),
                #         drawDropdown(list(df.flightnr.unique()),'flightnr_filter', 'Select a flight number')
                #         ]),
                #     dbc.Col([
                #         html.H6('Origin'),
                #         drawDropdown(list(df.origin.unique()), 'origin_filter', 'Select an airport')
                #         ])
                # ], width=5)
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.H6('Destination'),
                                        drawDropdownWithoutCard(list(df.dest.unique()), 'dest_filter', 'Select an airport', '100%'),
                                    ], width=6),
                                    # dbc.Col([
                                    #     html.H6('Origin'),
                                    #     drawDropdownWithoutCard(list(df.origin.unique()), 'origin_filter', 'Select an airport', '100%'),
                                    # ], width=4),
                                    dbc.Col([
                                        html.H6('Flight number'),
                                        drawDropdownWithoutCard(list(df.flightnr.unique()), 'flightnr_filter', 'Select a flight number', '100%'),
                                    ], width=6),
                                ]),
                            html.Br(),
                            html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        html.H6('Departure time from FRA'),
                                        drawRangeSliderWithoutCard(1, 'i1d2_')
                                        ], width = 12)
                                    ])
                            ])
                        )
                    ])
                ], width=5),
            ], align='center'),
            #     dbc.Col([
            #         dbc.Col([
            #             html.H6('Flight number'),
            #             html.Div([
            #                 dbc.Card(
            #                     dbc.CardBody([
            #                         drawDropdownWithoutCard(list(df.flightnr.unique()), 'flightnr_filter', 'Select a flight number'),
                                        
            #                             ]),
            #                     )]),
            #             # drawDropdown(list(df.flightnr.unique()),'flightnr_filter', 'Select a flight number')
            #             ]),
            #         dbc.Col([
            #             html.H6('Origin'),
            #             drawDropdown(list(df.origin.unique()), 'origin_filter', 'Select an airport')
            #             ])
            #     ], width=5),
            # ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawDonutChart(df, 'donut_chart1', 'Cargo volume [tonnes]')[0]]),
                dbc.Col([
                    drawDonutChart(df, 'donut_chart2', 'Cargo volume [tonnes]')[0]])
                ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawRangeSlider(1, 'i1d_')])
                #TODO: move range slider to filter card (so without the card)
                ]),
            # Data table
            dbc.Row([
                dbc.Col([
                    drawTable(df2, 'table1')])
                ]),
            # dbc.Row([
            #     dbc.Col([
            #         html.Img(src = './assets/IMG_0115.JPEG') 
            #     ], width=3),
            #     dbc.Col([
            #         html.Img(src = './assets/IMG_0115.JPEG')
            #     ], width=3),
            #     dbc.Col([
            #         html.Img(src = './assets/IMG_0115.JPEG')
            #     ], width=6),
            # ], align='center'), 
            # html.Br(),
            # dbc.Row([
            #     dbc.Col([
            #         html.Img(src = './assets/IMG_0115.JPEG')
            #     ], width=9),
            #     dbc.Col([
            #         html.Img(src = './assets/IMG_0115.JPEG')
            #     ], width=3),
            # ], align='center'),      
        ])
    )
])

# html.Img(src = './assets/IMG_0115.JPEG')

# Call backs

# Update table
@app.callback(
    Output('table1', 'data'),
    Input('flightnr_filter', 'value'),
    # Input('origin_filter', 'value'),
    Input('dest_filter', 'value')
    )
def update_table(flightnr, dest):
    if all(arg is None or len(arg) == 0 for arg in [flightnr, origin, dest]):
        data = df2.to_dict('records')
        return data
    else:
        # filtered_df = df2[df2.flightnr.isin(flightnr)
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        origin = list(df2['origin'].unique()) if origin in [None, []] else origin
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        print(f'{flightnr}, {origin}, {dest}')
        # origin = list(df2['origin']) # Dit lijkt te werken, maar dan moet dit ff eleganter? ff in-line if statement ofzo
        # dest = list(df2['dest'])
        filtered_df = df2[(df2.flightnr.isin(flightnr) & df2.origin.isin(origin) & df2.dest.isin(dest))]   # (df2['Age']<40) & df2['JOB'].str.startswith('P')]
        data = filtered_df.to_dict('records')
        return data
    
# Update (pie) chart
@app.callback(
    Output('donut_chart1', 'figure'),
    Input('flightnr_filter', 'value'),
    # Input('origin_filter', 'value'),
    Input('dest_filter', 'value')
    )
def update_pie_chart(flightnr, dest):
    if all(arg is None or len(arg) == 0 for arg in [flightnr, origin, dest]):
        fig = drawDonutChart(df, 'donut_chart1', 'Cargo volume [tonnes]')[1]
        return fig
    else:
        # filtered_df = df2[df2.flightnr.isin(flightnr)
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        origin = list(df2['origin'].unique()) if origin in [None, []] else origin
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        print(f'{flightnr}, {origin}, {dest}')
        # origin = list(df2['origin']) # Dit lijkt te werken, maar dan moet dit ff eleganter? ff in-line if statement ofzo
        # dest = list(df2['dest'])
        filtered_df = df2[(df2.flightnr.isin(flightnr) & df2.origin.isin(origin) & df2.dest.isin(dest))]   # (df2['Age']<40) & df2['JOB'].str.startswith('P')]
        fig = drawDonutChart(filtered_df, 'donut_chart1', 'Cargo volume [tonnes]')[1]
        return fig

#TODO: Fix the pie_chart updating

# Update map
@app.callback(
    Output('map', 'figure'),
    Input('flightnr_filter', 'value'),
    # Input('origin_filter', 'value'),
    Input('dest_filter', 'value')
          )
def update_flight_route(flightnr, dest): 
    if all(arg is None or len(arg) == 0 for arg in [flightnr, origin, dest]):
        flight_routes = getFlightRoutes(df)
        return (getmap('map', flight_routes)[1])
    else:
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        origin = list(df2['origin'].unique()) if origin in [None, []] else origin
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        filtered_df = df[(df.flightnr.isin(flightnr) & df.origin.isin(origin) & df.dest.isin(dest))]
        updated_flight_routes = getFlightRoutes(filtered_df)
        return (getmap('map', updated_flight_routes)[1])


# Update dropdown menus
# @app.callback(
#     Output('flightnr_filter', 'options'),
#     Output('origin_filter', 'options'),
#     Output('dest_filter', 'options'),
#     Input('flightnr_filter', 'value'),
#     Input('origin_filter', 'value'),
#     Input('dest_filter', 'value')
    
#     )
# def update_dropdown(flightnr, origin, dest):
#     if all(arg is None or len(arg) == 0 for arg in [flightnr, origin, dest]):
#         return (list(df.flightnr.unique()), list(df.origin.unique()), list(df.dest.unique()))
#     else:
#         # Ensure that when one or more options is != None, it doesn't crash
#         flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
#         origin = list(df2['origin'].unique()) if origin in [None, []] else origin
#         dest = list(df2['dest'].unique()) if dest in [None, []] else dest
#         filtered_df = df2[(df2.flightnr.isin(flightnr) & df2.origin.isin(origin) & df2.dest.isin(dest))]   # (df2['Age']<40) & df2['JOB'].str.startswith('P')]
#         return (list(filtered_df.flightnr.unique()), list(filtered_df.origin.unique()), list(filtered_df.dest.unique()))
    #TODO: Fix that when selecting only a single flight number, the other flight numbers remain visible
    # Hence, only update flight number drop down when a destination is selected
    # Maybe do a separte filtering per output and then don't filter for that specific dropdown's value?


#TODO: Fix isssue that causes me to use df and df2, will be cumbersome in the future
#TODO: Maybe combine the multiple call-backs? On the other hand, this gives more overview, but does have a lot of repeated code
#TODO: Add an option that toggles between the full dataframe (with individual shipments), and a dataframe that shows the totals per flight (number)
#TODO: Add options to include lay-overs as well?

















if __name__ == '__main__':
    app.run_server(debug=True)
