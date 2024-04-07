import plotly.graph_objects as go
import pandas as pd
from airport_data import df_airport
#%%

flightroutes = [([['FRA', 'ORD']], 2),
 ([['FRA', 'ORD'], ['ORD', 'LAX']], 2),
 ([['FRA', 'JFK']], 1),
 ([['BKK', 'SIN'], ['FRA', 'BKK']], 1),
 ([['ASB', 'HKG'], ['FRA', 'ASB']], 1),
 ([['FRA', 'BOM']], 1),
 ([['FRA', 'MAA'], ['MAA', 'DAC']], 1),
 ([['FRA', 'LEJ']], 1),
 ([['FRA', 'TAS']], 1),
 ([['FRA', 'LEJ']], 2),
 ([['FRA', 'JFK']], 2),
 ([['FRA', 'ORD'], ['ORD', 'IAH']], 2),
 ([['ATL', 'JFK'], ['FRA', 'ATL']], 2),
 ([['FRA', 'ATL']], 2),
 ([['FRA', 'ORD']], 3),
 ([['FRA', 'ORD'], ['ORD', 'DFW']], 2),
 ([['FRA', 'ORD'], ['ORD', 'MEX']], 1),
 ([['FRA', 'ORD'], ['MEX', 'GDL'], ['ORD', 'MEX']], 3),
 ([['FRA', 'ORD'], ['MEX', 'UIO'], ['ORD', 'MEX']], 2),
 ([['FRA', 'ORD'], ['ORD', 'LAX']], 2),
 ([['DKR', 'VCP'], ['FRA', 'DKR']], 1),
 ([['DKR', 'VCP'], ['FRA', 'DKR'], ['MVD', 'EZE'], ['VCP', 'MVD']], 1),
 ([['DKR', 'VCP'], ['FRA', 'DKR'], ['MVD', 'EZE'], ['VCP', 'MVD']], 1),
 ([['CWB', 'SCL'], ['DKR', 'VCP'], ['FRA', 'DKR'], ['VCP', 'CWB']], 1),
 ([['DKR', 'VCP'], ['FRA', 'DKR'], ['VCP', 'SCL']], 1),
 ([['CWB', 'SCL'], ['DKR', 'VCP'], ['FRA', 'DKR'], ['VCP', 'CWB']], 1),
 ([['FRA', 'CAI']], 3),
 ([['FRA', 'NBO'], ['NBO', 'JNB']], 1),
 ([['FRA', 'TLV'], ['TLV', 'IST']], 4),
 ([['BLR', 'HYD'], ['FRA', 'BLR']], 2),
 ([['FRA', 'BOM']], 1),
 ([['BOM', 'HYD'], ['FRA', 'BOM']], 1),
 ([['FRA', 'MAA'], ['MAA', 'DEL']], 1),
 ([['FRA', 'KJA'], ['KJA', 'NRT']], 3),
 ([['FRA', 'SVO'], ['SVO', 'NRT']], 2),
 ([['FRA', 'KJA'], ['KJA', 'PEK']], 3),
 ([['FRA', 'KJA'], ['KJA', 'PEK'], ['PEK', 'ICN']], 2),
 ([['FRA', 'PVG']], 7),
 ([['FRA', 'KJA'], ['KJA', 'PVG']], 2),
 ([['FRA', 'KJA'], ['ICN', 'CKG'], ['KJA', 'ICN']], 2),
 ([['ALA', 'CAN'], ['FRA', 'ALA']], 3),
 ([['DMM', 'SHJ'], ['FRA', 'DMM'], ['SHJ', 'HKG']], 1),
 ([['BOM', 'HKG'], ['FRA', 'BOM']], 1),
 ([['FRA', 'RUH'], ['RUH', 'SHJ'], ['SHJ', 'HKG']], 1),
 ([['DEL', 'HKG'], ['FRA', 'DEL']], 1),
 ([['BOM', 'HKG'], ['FRA', 'BOM']], 1)]

# df_flight_paths = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_aa_flight_paths.csv')
# df_flight_paths.head()

def test():
    # df_airport1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
    # df_airport1.head()
    
    # df_flight_paths = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_aa_flight_paths.csv')
    # df_flight_paths.head()
    
    fig = go.Figure(go.Scattergeo())
    
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_airport['lon'],
        lat = df_airport['lat'],
        hoverinfo = 'text',
        text = df_airport["iata"] + ' - ' + df_airport['name'],
        mode = 'markers',
        marker = dict(
            size = 2,
            color = 'rgb(255, 0, 0)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))
    max_ = 0
    for i in flightroutes:
        max_ = i[-1] if i[-1] > max_ else max_
        
    for routes in flightroutes:
        for leg in routes[0]:
            max_ = 7
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
                    #TODO: add opacity based # flightnumbers / max total flight number
                      
                        # opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
                        ))
    
    # for i in range(len(df_flight_paths)):
    #     fig.add_trace(
    #         go.Scattergeo(
    #             locationmode = 'USA-states',
    #             lon = [df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i]],
    #             lat = [df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i]],
    #             mode = 'lines',
    #             line = dict(width = 1,color = 'red'),
    #             opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
    #         )
    #     )
    fig.update_layout(
        title_text = 'Feb. 2011 American Airline flight paths<br>(Hover for airport names)',
        showlegend = False,
        geo = dict(
            scope = 'world',
            projection_type = 'natural earth',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
            # center = dict(lat=0, lon=0),  # Center the map at (0,0)
            # projection_scale=1.0,         # Adjust the scale of the projection
            # # Set initial zoom level
            # lataxis = dict(range=[-50, 80]),  # Latitude range
            # lonaxis = dict(range=[-180, 180])  # Longitude range
        ),
        width = 1000,
        height = 600
    )
    return(fig)



test().write_html('./test.html')

# https://plotly.com/python/lines-on-maps/

# https://community.plotly.com/t/dash-bootstrap-templates/52456