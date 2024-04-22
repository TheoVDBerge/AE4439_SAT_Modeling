# Import required libraries
import dash
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dash_table as dt
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input
from dash.dependencies import Output
import dash_bootstrap_components as dbc
import plotly.express as px
from main_data import df
print('Imported main_data.py')
from airport_data import df_airport
print('Imported airport data')
from helper_functions import getFlightRoutes, getHHMM
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

def drawRangeSliderWithoutCard(data_, id_, min_, max_, ds_label, ds_mark, datatype):
    marks_ = {}      
    if datatype == 'time':
        marks_ =  {str(round(k, 2)): {'label': f'{round(k, 2)}:00',
                     'style': {'transform':'rotate(45deg)'}} for k in np.arange(min_,max_+1)}
        value_ = [5,15]
        
    elif datatype == 'lf':
        marks_ =  {str(round(k, 2)): {'label': "{:.2f}".format(float(round(k, 2))),
                     'style': {'transform':'rotate(45deg)'}} for k in np.arange(min_, max_ + ds_label, ds_label)}
        value_ = [0.25, 0.75]
        
    return(dcc.RangeSlider(min_, max_, ds_mark,
    # TODO: add different variable for ds for marks and ds for labels
        marks = marks_,
        value = value_,
        id = id_,
        allowCross = False
        ), marks_)

def drawRangeSlider(data_, id_, min_, max_, ds, datatype):
    return(html.Div([
        dbc.Card(
            dbc.CardBody([
                 drawRangeSliderWithoutCard(data_, id_, min_, max_, ds, datatype) 
                ])
            )
        ])
        )

def drawBarChart(data_, id_, type_):
    if type_ == 'frequency':
        #TODO: Group departures per one hour timeslots
        data__ = data_.drop_duplicates(subset = ['date', 'flightnr'])['std'].value_counts()
        fig = px.bar(data__, x = data__.index, y = data__)

    elif type_ == 'lf':
        # The data here is extracted from the df into a list, turned into a dataFrame and back to a Series.... Probably there is a cleaner way
        # but this is what I came up with for now and filters what I want
        data__ = pd.DataFrame([(data_[(data_.uniqueflightid == x)].lf.sum()) for x in data_.uniqueflightid.unique()], index = [x for x in df.uniqueflightid.unique()]).squeeze()
        # data__ = pd.DataFrame([(data_[(data_.uniqueflightid == x)].lf.sum()) for x in data_.uniqueflightid.unique()], index = [x.split('-')[0] for x in df.uniqueflightid.unique()]).squeeze()
        fig = px.bar(data__, x = data__.index , y = data__.values)

    
    fig.update_layout(       
       template = 'plotly_dark',
       xaxis_tickangle = -45,
#TODO: Add still axis labels
        )
    return(html.Div([
        dbc.Card(
            dbc.CardBody([dcc.Graph(id = id_,
                      figure = fig)
                ])
            
            )
        ])
        )
    


#%%
unique_flights = df.uniqueflightid.unique()
test = df.drop_duplicates('uniqueflightid')['std']

deptimes = [0] * 25
for time in test:
    time_ = int(time[0:2])
    deptimes[time_] += 1

#%%
def drawLineChart(data_, id_, title_, type_):
    
    if type_ == 'daily':
        
        xlabel_ = 'Day'
        ylabel_ = 'Occurences'
        
        def getData():
            depcat = [0] * 25
            deptimes = [f'{x}:00' for x in range(0,25)]
            
            depdata = df.drop_duplicates('uniqueflightid')['date']
            
            for date in depdata:
                date_ = int(date.split('-')[-1])
                depcat[date_] += 1
            return(deptimes, depcat)
        
    elif type_ == 'hourly':
        
        xlabel_ = 'Time'
        ylabel_ = 'Occurences'
        
        def getData():
            depcat = [0] * 25
            deptimes = [f'{x}:00' for x in range(0,25)]
            
            depdata = df.drop_duplicates('uniqueflightid')['std']
            
            for time in depdata:
                time_ = int(time.split(':')[0])
                depcat[time_] += 1
            return(deptimes, depcat)
    
    
    
    fig = px.line(x = getData()[0],
                  y = getData()[1],
                  # title = 'Test',
                  labels = {'x': xlabel_, 'y': ylabel_},
                  markers = True,
                  color_discrete_sequence=["yellow"])
    
    fig.update_layout(
       title={'text': title_, 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
       xaxis_tickangle = -45,
       template = 'plotly_dark'
   )
    
    return(html.Div([
        dbc.Card(
            dbc.CardBody([dcc.Graph(id = id_,
                      figure = fig)
                ])
            
            )
        ])
        )


# Main website lay-out
# app.layout = html.Div(style={'width':'80%', 'margin':'auto'}, children=[
app.layout = html.Div(children=[
    # Main body of the website, this card holds everything
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
                # This column/card holds all filter options
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
                                dbc.Row([
                                    dbc.Col([
                                        html.H6('Dangerous goods'),
                                        drawDropdownWithoutCard(list(df.specials.unique()), 'specials_filter', 'Select an option', '100%'),
                                    ], width = 6),
                                    dbc.Col([
                                        html.H6('Data options'),
                                        dcc.RadioItems(
                                            options=['Shipments', 'Flights'],
                                            value='Shipments',
                                            inline=True,
                                                    ),
                                    ], width = 6),
                                ]),
                            html.Br(),
                            html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        html.H6('Departure time from FRA (05:00-15:00)', id = 'H6-dep'),
                                        drawRangeSliderWithoutCard(df, 'slider-dep', 0, 24, 1, 0.25, 'time')[0]
                                        ], width = 12)
                                    ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.H6('Load factor', id = 'H6-lf'),
                                        drawRangeSliderWithoutCard(df, 'slider-lf', 0, 1, 0.05, 0.05, 'lf')[0]
                                        ], width = 12)
                                    ]),
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
                    # drawDonutChart(df, 'donut_chart1', 'Cargo volume [tonnes]')[0]]),
                    drawLineChart(df, 'testt2', 'FRA daily departure occurences', 'daily')]),
                dbc.Col([
                    drawLineChart(df, 'testtt', 'FRA hourly departure occurences', 'hourly'),
                    ])
                ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawBarChart(df, 'blabla', 'frequency')]),
                dbc.Col([
                    drawBarChart(df, 'blabla', 'lf')])
                ]),
            html.Br(),
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
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest]):
        data = df2.to_dict('records')
        return data
    else:
        # filtered_df = df2[df2.flightnr.isin(flightnr)
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        # origin = list(df2['origin'].unique()) if origin in [None, []] else origin
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        print(f'{flightnr}, {dest}')
        # origin = list(df2['origin']) # Dit lijkt te werken, maar dan moet dit ff eleganter? ff in-line if statement ofzo
        # dest = list(df2['dest'])
        filtered_df = df2[(df2.flightnr.isin(flightnr) & df2.dest.isin(dest))]   # (df2['Age']<40) & df2['JOB'].str.startswith('P')]
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
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest]):
        fig = drawDonutChart(df, 'donut_chart1', 'Cargo volume [tonnes]')[1]
        return fig
    else:
        # filtered_df = df2[df2.flightnr.isin(flightnr)
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        print(f'{flightnr}, {dest}')
        # origin = list(df2['origin']) # Dit lijkt te werken, maar dan moet dit ff eleganter? ff in-line if statement ofzo
        # dest = list(df2['dest'])
        filtered_df = df2[(df2.flightnr.isin(flightnr) & df2.dest.isin(dest))]   # (df2['Age']<40) & df2['JOB'].str.startswith('P')]
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
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest]):
        flight_routes = getFlightRoutes(df)
        return (getmap('map', flight_routes)[1])
    else:
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        filtered_df = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest))]
        updated_flight_routes = getFlightRoutes(filtered_df)
        return (getmap('map', updated_flight_routes)[1])

# Update text for slidesr
@app.callback(
    Output('H6-dep', 'children'),
    Output('H6-lf', 'children'),
    Input('slider-dep', 'value'),
    Input('slider-lf', 'value')
    )

def update_slider(dep, lf):
    time1 = getHHMM(dep[0]) 
    time2 = getHHMM(dep[1])
    return(f'Departure time at FRA: ({time1}-{time2})', f'Load factor: ({lf[0]}-{lf[1]})')


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
#TODO: Add plot for: departure tiem (bar chart), frequency per day (line chart), load factor (line chart?)
#TODO: use the new index to plot frequency and load factor as bar chart
















if __name__ == '__main__':
    app.run_server(debug=True)
