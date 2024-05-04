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
from helper_functions import getFlightRoutes, getHHMM, getDayOfWeek
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
# Flattening the list will be done here and not in the main_data, as it will break the getmap function and i don't feel like fixing it
df2 = df.drop(columns=['route'])

def getAirportNames(airports):
    temp_dropdown = []
    temp = []
    for airport in airports:
        temp_dropdown.append({'label': f'{airport} - {df_airport[df_airport.iata == airport].city[0]}', 'value': f'{airport}'})
        temp.append(f'{airport}') 
    return(temp_dropdown, temp)


#%%
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
        title_text = 'Flown legs for selected data (hover for airport names)',
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
        # Style headers
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        },
        
        # Style cells
        style_cell={
            'backgroundColor': 'rgb(255, 255, 255)',
            'color': 'black',
            'padding': '10px',
            'textAlign': 'left'
        },
        
        # Style data conditionally
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(240, 240, 240)'
            }
        ],

        # Set the table to be interactive
        filter_action="native",  # Enable filtering
        sort_action = "native",    # Enable sorting
        page_action = "native",    # Enable pagination
        page_size = 50             # Number of rows per page
    
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
            labels = getAirportNames(list(df.dest.unique()))[1],
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
        value_ = [0,23]
        
    elif datatype == 'lf':
        marks_ =  {str(round(k, 2)): {'label': "{:.2f}".format(float(round(k, 2))),
                     'style': {'transform':'rotate(45deg)'}} for k in np.arange(min_, max_ + ds_label, ds_label)}
        value_ = [0, 1]
        
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

def drawBarChart(data_, id_, type_, title_):
    if type_ == 'volume':
        #TODO: Add percentages to the labels
        # Create a list of lists with the required data [[Destination], [Volume]]
        data__ = [list(data_.dest.unique()), [(data_[data_.dest.isin([x])]['totalWeight'].sum()/1000) for x in list(data_.dest.unique())]]
        
        # Turn this list of lists into a DataFrame for better handling by Dash, where each nested list is a column
        df_volume = pd.DataFrame(zip(*data__), columns = ['Destination', 'Volume']).sort_values(by='Volume', ascending = False)
        
        fig = px.bar(df_volume, 
                     x = 'Destination',
                     y = 'Volume',
                     labels = {'Destination': 'Destination', 'Volume': 'Volume [tonnes]'},
                     color_discrete_sequence = ['#ffb500']
                     )
        
        fig.update_layout(
            title={'text': title_, 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
            template = 'plotly_dark',
            xaxis_tickangle = -45,
            )

    elif type_ == 'lf':
        
        # Extract the required load factors, based on date (primary)
        # and flightnr (secondary). Then, the load factor is calculated
        # for each individual flight per day.
        sorted_data = data_.groupby(['date', 'flightnr'])['lf'].sum()
        
        # Due to the double indexing, I extract the unique values of 
        # both levels of indexes.
        unique_dates = sorted_data.index.get_level_values('date').unique()
        unique_flightnr = sorted_data.index.get_level_values('flightnr').unique()

        # Rearrange the data so that it becomes a list of lists, where the list
        # has len(unique_dates) and each nested list len(unique_flightnr).
        # In other words, every list is a day of the week where all flight numbers
        # are represented. 
        daily_data = []

        for flight in unique_dates:
            temp = []
            for date in unique_flightnr:
                try:
                    temp.append(sorted_data[flight][date])
                except:
                    # In case of flight not being operated on a day of the week,
                    # a lf of 0 is added. This is required to keep track of the
                    # different flight numbers whilst plotting.
                    temp.append(0)
            
            daily_data.append(temp)
            
        # Create a final dictionary that will ease the plotting
        final_data = {getDayOfWeek(unique_dates[i])[1]: daily_data[i] for i in range(len(unique_dates))}
            
        # Create a figure object
        fig = go.Figure()

        # Loop through the final_data to create a bar for each day of the week
        for day, values in final_data.items():
            fig.add_trace(go.Bar(name=day, x=unique_flightnr, y=values))

        fig.update_layout(barmode='stack')
    
    fig.update_layout(
        title={'text': title_, 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
       template = 'plotly_dark',
       xaxis_tickangle = -45,
        )
    return(html.Div([
        dbc.Card(
            dbc.CardBody([dcc.Graph(id = id_,
                      figure = fig)
                ])
            
            )
        ])
        , fig)

def drawLineChart(data_, id_, title_, type_):
    
    depdata = data_.drop_duplicates('uniqueflightid')['datetimeobject']
    
    if type_ == 'daily':
        
        deptimes = ['Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday', 'Sunday']
        
        xlabel_ = 'Day'
        ylabel_ = 'Occurences'
        
        depcat = [0] * 7
        for date in depdata:
            date_ = date.weekday()
            depcat[date_] += 1
        
    elif type_ == 'hourly':
        
        deptimes = [f'{x}:00' for x in range(0,25)]
        
        xlabel_ = 'Time'
        ylabel_ = 'Occurences'
        
        depcat = [0] * 25
        for time in depdata:
            time_ = time.hour
            depcat[time_] += 1
            
    fig = px.line(x = deptimes,
                  y = depcat,
                  # title = 'Test',
                  labels = {'x': xlabel_, 'y': ylabel_},
                  markers = True,
                  color_discrete_sequence=["yellow"])
    
    fig.update_yaxes(ticklabelstep=2)
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
        ]), fig
        )

def drawHistogram(data_, id_, title_, type_):
    
    depdata = data_.drop_duplicates('uniqueflightid')['datetimeobject']
    
    if type_ == 'daily':
        
        deptimes = ['Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday', 'Sunday']
        
        xlabel_ = 'Day'
        ylabel_ = 'Occurences'
        range_ = [-0.5,6.5]
        n_bins = 7
        
        depcat = [0] * 7
        for date in depdata:
            date_ = date.weekday()
            depcat[date_] += 1
        
    elif type_ == 'hourly':
        
        deptimes = [f'{x}:00' for x in range(0,25)]
        
        xlabel_ = 'Time'
        ylabel_ = 'Occurences'
        range_ = [0,25]
        n_bins = 25

        # This could have been done cleaner, but I already wrote this code for the line charts
        # and this format works well for hour and day based data. Days of the week (strings) are not countable
        # which messes up the ordering of the bar chart. Sticking to the old method gives the desired result.
        depcat = [0] * 25
        for time in depdata:
            time_ = time.hour
            depcat[time_] += 1
            
    fig = px.histogram(x = deptimes,
                       y = depcat,
                       nbins = n_bins,
                       color_discrete_sequence=["#ffb500"])
    
    fig.update_layout(
       title={'text': title_, 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
       xaxis_tickangle = -45,
       bargap = 0.1,
       yaxis_title = ylabel_,
       xaxis_title = xlabel_,
       xaxis_range = range_,
       template = 'plotly_dark'
    )
    
    return(html.Div([
        dbc.Card(
            dbc.CardBody([dcc.Graph(id = id_,
                      figure = fig)
                ])
            
            )
        ]), fig
        )
    
# This function will be used to filter for load factor in the table and graphs
def getLFFlights(data_, ll, ul):
    # Get a summed list (Panda Series) of unique flights with respective load factors
    # The data here is extracted from the df into a list, turned into a dataFrame and back to a Series.... Probably there is a cleaner way
    # but this is what I came up with for now and does what I want
    summedLF = pd.DataFrame([(df[(df.uniqueflightid == x)].lf.sum()) for x in df.uniqueflightid.unique()], index = [x for x in df.uniqueflightid.unique()]).squeeze()
    filtered_LF = summedLF[summedLF.between(ll, ul)] # Extract the rows that are between this range
    flightnr_ = [x.split('-')[0] for x in filtered_LF.index]
    return(flightnr_)

def getFlightDF(data_):
    sorted_data = data_.groupby(['uniqueflightid'])[['numpieces', 'totalWeight', 'lf']].sum()
    new_df = data_.drop_duplicates('uniqueflightid')
    for i, j in zip(new_df.index, new_df.uniqueflightid):
        new_df.loc[i, ['numpieces', 'totalWeight', 'lf']] = list(sorted_data.loc[j])
        new_df.loc[i, ['specials']] = 'N/A'
    return(new_df)

# def flatten(input_):
#     temp = []
#     for lst in input_:
#         if isinstance(lst, list):
#             for nested_list in lst:
#                 temp.append(nested_list)
#         else:
#             temp.append()
#     return(temp)

# def flattenRoute(data_):
    
#     def removeDuplicateStrings(input_):
#         seen = set()
#         result = []
#         for item in flatten(input_):
#             if item not in seen:
#                 seen.add(item)
#                 result.append(item)
    
#     new_df = data_
#     for i, j in zip(data_.index, data_.route):
#         new_df.loc[i, ['route']] = removeDuplicateStrings(j)
        
#     return(new_df)


test = getFlightDF(df)

#%%
unique_flights = df.uniqueflightid.unique()
test = df.drop_duplicates('uniqueflightid')['std']

deptimes = [0] * 25
for time in test:
    time_ = int(time[0:2])
    deptimes[time_] += 1

#%%


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
                                        drawDropdownWithoutCard(getAirportNames(list(df.dest.unique()))[0], 'dest_filter', 'Select an airport', '100%'),
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
                                        dcc.RadioItems(id = 'dataSelection',
                                            options=['Shipments', 'Flights'],
                                            value='Shipments',
                                            inline=True,
                                            inputStyle={"margin-right": "10px",
                                                        "margin-left": "10px"},
                                                    ),
                                    ], width = 4),
                                    dbc.Col([
                                        html.Button('Reset', id = 'ResetButton',
                                                    style = {"margin-top": "20px",
                                                             "margin-right": "5px"}),
                                        ], width = 2)
                                ]),
                            html.Br(),
                            html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        html.H6('Departure time from FRA (00:00-23:00)', id = 'H6-dep'),
                                        drawRangeSliderWithoutCard(df, 'slider-dep', 0, 23, 1, 0.25, 'time')[0]
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
                    drawHistogram(df, 'dailydep', 'FRA daily departures', 'daily')[0]
                    ]),
                dbc.Col([
                    drawHistogram(df, 'hourlydep', 'FRA hourly departures', 'hourly')[0],
                    ])
                ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawBarChart(df, 'TotalVolume', 'volume', 'Transported volume [tonnes]')[0]]),
                dbc.Col([
                    drawBarChart(df, 'TotalLF', 'lf', 'Load factor')[0]])
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
    Input('dest_filter', 'value'),
    Input('slider-dep', 'value'),
    Input('slider-lf', 'value'),
    Input('dataSelection', 'value')
    )
def update_table(flightnr, dest, time_, lf, type_):
    
    if type_ == 'Shipments':
        df_table = df2
    elif type_ == 'Flights':
        df_table = getFlightDF(df2)
    
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest, time_, lf]):
        data = df_table.to_dict('records')
        return data
    else:
        flightnr = list(df_table['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df_table['dest'].unique()) if dest in [None, []] else dest
        # Filter flight number, destination, departure time, load factor
        filtered_df_table = df_table[(df_table.flightnr.isin(flightnr) & df_table.dest.isin(dest) & df_table['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df_table.flightnr.isin(getLFFlights(df_table, lf[0], lf[1])))].drop(columns=['datetimeobject'])
        data = filtered_df_table.to_dict('records')
        return data
    
#TODO: Ensure that the other charts, as well as the map, now also updates based on the filters
#TODO: Remove date-time object still
    
# # Update (pie) chart
# @app.callback(
#     Output('donut_chart1', 'figure'),
#     Input('flightnr_filter', 'value'),
#     # Input('origin_filter', 'value'),
#     Input('dest_filter', 'value')
#     )
# def update_pie_chart(flightnr, dest):
#     if all(arg is None or len(arg) == 0 for arg in [flightnr, dest]):
#         fig = drawDonutChart(df, 'donut_chart1', 'Cargo volume [tonnes]')[1]
#         return fig
#     else:
#         # filtered_df = df2[df2.flightnr.isin(flightnr)
#         flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
#         dest = list(df2['dest'].unique()) if dest in [None, []] else dest
#         print(f'{flightnr}, {dest}')
#         # origin = list(df2['origin']) # Dit lijkt te werken, maar dan moet dit ff eleganter? ff in-line if statement ofzo
#         # dest = list(df2['dest'])
#         filtered_df = df2[(df2.flightnr.isin(flightnr) & df2.dest.isin(dest))]   # (df2['Age']<40) & df2['JOB'].str.startswith('P')]
#         fig = drawDonutChart(filtered_df, 'donut_chart1', 'Cargo volume [tonnes]')[1]
#         return fig

# #TODO: Fix the pie_chart updating

# Update map
@app.callback(
    Output('map', 'figure'),
    Input('flightnr_filter', 'value'),
    Input('dest_filter', 'value'),
    Input('slider-dep', 'value'),
    Input('slider-lf', 'value')
          )
def update_flight_route(flightnr, dest, time_, lf): 
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest, time_, lf]):
        flight_routes = getFlightRoutes(df)
        return (getmap('map', flight_routes)[1])
    else:
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
         
        # filtered_df = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest) & df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df.flightnr.isin(getLFFlights(df2, lf[0], lf[1])))].drop(columns=['datetimeobject'])
        filtered_df_map = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest) & df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df.flightnr.isin(getLFFlights(df2, lf[0], lf[1])))]
        updated_flight_routes = getFlightRoutes(filtered_df_map)
        return (getmap('map', updated_flight_routes)[1])

# Update text for sliders
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

# Update histogram charts
@app.callback(
    Output('dailydep', 'figure'),
    Output('hourlydep', 'figure'),
    Input('flightnr_filter', 'value'),
    Input('dest_filter', 'value'),
    Input('slider-dep', 'value'),
    Input('slider-lf', 'value')
          )
def update_line_chart(flightnr, dest, time_, lf):
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest, time_, lf]):
        fig = drawLineChart(df, 'dailydep', 'FRA daily departures', 'daily')[1]
        return fig
    else:
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
         
        filtered_df_line = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest) & df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df.flightnr.isin(getLFFlights(df2, lf[0], lf[1])))]
        
        fig_daily = drawHistogram(filtered_df_line, 'dailydep', 'FRA daily departures', 'daily')[1]
        fig_hourly = drawHistogram(filtered_df_line, 'hourlydep', 'FRA hourly departures', 'hourly')[1]
        return(fig_daily, fig_hourly)


# Update bar chart
# @app.callback(
#     Output('TotalVolume', 'figure'),
#     Output('TotalLF', 'figure'),
#     Input('flightnr_filter', 'value'),
#     Input('dest_filter', 'value'),
#     Input('slider-dep', 'value'),
#     Input('slider-lf', 'value')
#           )
# def update_bar_chart(flightnr, dest, time_, lf):
#     if all(arg is None or len(arg) == 0 for arg in [flightnr, dest, time_, lf]):
#         fig = drawLineChart(df, 'dailydep', 'FRA daily departures', 'daily')[1]
#         return fig
#     else:
#         flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
#         dest = list(df2['dest'].unique()) if dest in [None, []] else dest
         
#         filtered_df_bar = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest) & df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df.flightnr.isin(getLFFlights(df2, lf[0], lf[1])))]
#         print(f'{flightnr}, {dest}, {time_}, {lf}')
        
#         fig_volume = drawBarChart(filtered_df_bar, 'TotalVolume', 'volume', 'Transported volume')[1]
#         fig_lf= drawBarChart(filtered_df_bar, 'TotalLF', 'lf', 'Load factor')[1]
#         return(fig_volume, fig_lf)
    
# Update bar chart
@app.callback(
    Output('TotalVolume', 'figure'),
    Output('TotalLF', 'figure'),
    Input('flightnr_filter', 'value'),
    Input('dest_filter', 'value'),
    Input('slider-dep', 'value'),
    Input('slider-lf', 'value')
          )
def update_bar_chart(flightnr, dest, time_, lf):
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest, time_, lf]):
        fig_volume = drawLineChart(df, 'dailydep', 'FRA daily departures', 'daily')[1]
        fig_lf = drawBarChart(df, 'TotalLF', 'lf', 'Load factor')[1]
        return(fig_volume, fig_lf)
    else:
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
         
        filtered_df_bar = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest) & df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df.flightnr.isin(getLFFlights(df2, lf[0], lf[1])))]
        
        fig_volume = drawBarChart(filtered_df_bar, 'TotalVolume', 'volume', 'Transported volume [tonnes]')[1]
        fig_lf = drawBarChart(filtered_df_bar, 'TotalLF', 'lf', 'Cargo load factor')[1]
        return(fig_volume, fig_lf)

# Update button
@app.callback(
    Output('flightnr_filter', 'value'),
    Output('dest_filter', 'value'),
    Output('slider-dep', 'value'),
    Output('slider-lf', 'value'),
    Output('dataSelection', 'value'),
    Input('ResetButton', 'n_clicks'),
    prevent_initial_call = True
    )

def update_filters(value1):
    flightfilter, destinations = None, None
    slider1, slider2 = [0,23], [0,1]
    radioItem = 'Shipments'
    return(flightfilter, destinations, slider1, slider2, radioItem)
    
#TODO: Fix this updating



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
#TODO: Add a README where the package versions of all the used packages are described, as well as a quick overview of the code.
















if __name__ == '__main__':
    app.run_server(debug=True)
