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
from main_data import df, arrangeAirports
print('Imported main_data.py')
from airport_data import df_airport
print('Imported airport data')
from helper_functions import getFlightRoutes, getHHMM, getDayOfWeek, getPayload, getDistance
print('Imported helper_functions.py')
#%%
print('Imported all requirements')

flight_routes = getFlightRoutes(df)

print('Initialised flight routes')

# Initialize the app
app = Dash(__name__)
app.title = 'SAT modeling project'

print('Initialised the web-app')

# Flattening the list will be done here and not in the main_data, as it will break the getmap function
df2 = df.drop(columns=['route'])


# Generate airport names (IATA code + name) for the dropdowns
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
    )
    return (html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(id = id_,
                          figure = fig)
            ])
        )
    ]), fig)


# Draw a drop-down menu without the card body
def drawDropdownWithoutCard(options_, id_, placeholder_, width_):
    # Options must be a list
    return(dcc.Dropdown(
                    id = id_,
                    options = options_,
                    placeholder = placeholder_,
                    multi = True,
                    style = {'width': width_})                  
        )

# Draw a drop-down menu with the card body
def drawDropdown(options_, id_, placeholder_, width_):
    # Options must be a list
    return(html.Div([
        dbc.Card(
            dbc.CardBody([
                drawDropdownWithoutCard(options_, id_, placeholder_, width_),
                    
                    ]),
            )])
        )

# Draw the table
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
        filter_action="native",    # Enable filtering
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

# Draw the filter slider without the card body
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
        marks = marks_,
        value = value_,
        id = id_,
        allowCross = False
        ), marks_)

# Draw the filter slider with the card body
def drawRangeSlider(data_, id_, min_, max_, ds, datatype):
    return(html.Div([
        dbc.Card(
            dbc.CardBody([
                 drawRangeSliderWithoutCard(data_, id_, min_, max_, ds, datatype) 
                ])
            )
        ])
        )

# Draw a bar chart
def drawBarChart(data_, id_, type_, title_):
    # if-statement to re-use the same function multiple times
    if type_ == 'volume':
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
            xaxis_tickangle = -90,
            )

    elif type_ == 'lf':        
        fig = px.bar(data_, x='Flight number', y='LoadFactor', color='Day',
                     hover_data=['legs'], barmode='stack',
                     title="Load Factor by Flight Number Across Different Days",
                     labels={"FlightNumber": "Flight number", "LoadFactor": "Load factor"},
                     )
    
        fig.update_layout(
            title={'text': title_, 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
            xaxis = {'categoryorder': 'total descending'},
            yaxis_title = 'Load factor',
            template = 'plotly_dark',
            xaxis_tickangle = -90,
            )
    # Please note that in most instances where a figure/graph is being generated, two elements are being returned.
    # First, the entire figure + card body is being returned - this is for the initial boot-up. Secondly, only the 'figure' element
    # is being returned. This is used by the call-backs, as a figure (fig element) needs to be used as output for the callback, hence
    # without the card body elements.
    return(html.Div([
        dbc.Card(
            dbc.CardBody([dcc.Graph(id = id_,
                      figure = fig)
                ])
            )
        ])
        , fig)

# Draw a line chart
def drawLineChart(data_, id_, title_, type_):
    
    depdata = data_.drop_duplicates('uniqueflightid')['datetimeobject']
    
    # If-statements to allow multiple uses of the same function.
    if type_ == 'daily':
        
        deptimes = ['Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday', 'Sunday']
        
        xlabel_ = 'Day'
        ylabel_ = 'Occurences'
        
        # Generate labels for the x-axis
        depcat = [0] * 7
        for date in depdata:
            date_ = date.weekday()
            depcat[date_] += 1
        
    elif type_ == 'hourly':
        
        deptimes = [f'{x}:00' for x in range(0,25)]
        
        xlabel_ = 'Time'
        ylabel_ = 'Occurences'
        
        # Generate labels for the x-axis
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
    
    # Once again, two elements are being returned here - as has been discussed above.
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

def getLFFlights2(data_):
    sorted_data = data_.groupby(['date', 'flightnr', 'leg'])['totalWeight'].sum()

    unique_dates = sorted_data.index.get_level_values('date').unique()
    
    days = []
    dates = []
    flightnr = []
    legs = []
    load_factors = []

    for day in unique_dates:
        for flight in sorted_data[day].index.get_level_values('flightnr').unique():
            for num, leg in enumerate(arrangeAirports(sorted_data[day].loc[flight].index.get_level_values('leg'))):
                days.append(getDayOfWeek(day)[1])
                dates.append(day)
                flightnr.append(flight)
                legs.append(leg)
                load_factors.append(round((sorted_data[day][flight].iloc[num:].sum())/getPayload(getDistance(df_airport, leg)), 2))
                
    df_lf = pd.DataFrame({
        'Day': days,
        'Date': dates,
        'Flight number': flightnr,
        'legs': legs,
        'LoadFactor': load_factors
    })
       
    return(df_lf)

# For the table to show only flights, and not only shipments
def getFlightDF(data_):
    sorted_data = data_.groupby(['uniqueflightid'])[['numpieces', 'totalWeight', 'lf']].sum()
    new_df = data_.drop_duplicates('uniqueflightid')
    for i, j in zip(new_df.index, new_df.uniqueflightid):
        new_df.loc[i, ['numpieces', 'totalWeight', 'lf']] = list(sorted_data.loc[j])
        new_df.loc[i, ['specials']] = 'N/A'
    return(new_df)

def getDangerousGoods():
    IATAcodes = []
    for i in df.specials.unique():
        try:
            if len(i.split()) != 0:
                for j in i.split():
                    IATAcodes.append(j)
                
        except:
            pass
    return(IATAcodes)

#%%
unique_flights = df.uniqueflightid.unique()
test = df.drop_duplicates('uniqueflightid')['std']

deptimes = [0] * 25
for time in test:
    time_ = int(time[0:2])
    deptimes[time_] += 1

#%%


# Main website lay-out
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
                                        drawDropdownWithoutCard(getDangerousGoods(), 'specials_filter', 'Select an option', '100%'),
                                    ], width = 6),
                                    dbc.Col([
                                        html.H6('Data options'),
                                        dcc.RadioItems(id = 'dataSelection',
                                            options=['Flights', 'Shipments'],
                                            value='Flights',
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
            html.Br(),
            dbc.Row([
                dbc.Col([
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
                    drawBarChart(getLFFlights2(df), 'TotalLF', 'lf', 'Load factor')[0]])
                ]),
            html.Br(),
            # Data table
            dbc.Row([
                dbc.Col([
                    drawTable(df2, 'table1')])
                ]),     
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
@app.callback(
    Output('TotalVolume', 'figure'),
    Output('TotalLF', 'figure'),
    Input('flightnr_filter', 'value'),
    Input('dest_filter', 'value'),
    Input('specials_filter', 'value'),
    Input('slider-dep', 'value'),
    Input('slider-lf', 'value')
          )
def update_bar_chart(flightnr, dest, IATA, time_, lf):
    if all(arg is None or len(arg) == 0 for arg in [flightnr, dest, time_, lf]):
        fig_volume = drawLineChart(df, 'dailydep', 'FRA daily departures', 'daily')[1]
        fig_lf = drawBarChart(df, 'TotalLF', 'lf', 'Load factor')[1]
        return(fig_volume, fig_lf)
    else:
        flightnr = list(df2['flightnr'].unique()) if flightnr in [None, []] else flightnr
        dest = list(df2['dest'].unique()) if dest in [None, []] else dest
        print(flightnr)
        print(dest)
        print(time_)
        print(lf)
        
        df_lf = getLFFlights2(df)
        
        result_df = df_lf[(df_lf['LoadFactor'] > lf[0]) & (df_lf['LoadFactor'] < lf[1])]
        
        time_flightnr = df[df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time())].flightnr.unique()
        dest_flightnr = df[df.dest.isin(dest)].flightnr.unique()
        
        result_df2 = result_df[result_df['Flight number'].isin(flightnr) & result_df['Flight number'].isin(time_flightnr) & result_df['Flight number'].isin(dest_flightnr)]
        
        
        filtered_df_bar = df[(df.flightnr.isin(flightnr) & df.dest.isin(dest) & df['datetimeobject'].dt.time.between(pd.Timestamp(getHHMM(time_[0])).time(), pd.Timestamp(getHHMM(time_[1])).time()) & df.flightnr.isin(getLFFlights(df2, lf[0], lf[1])))]
        
        fig_volume = drawBarChart(filtered_df_bar, 'TotalVolume', 'volume', 'Transported volume [tonnes]')[1]
        fig_lf = drawBarChart(result_df2, 'TotalLF', 'lf', 'Cargo load factor')[1]
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


if __name__ == '__main__':
    app.run_server(debug=True)
   