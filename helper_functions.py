import pandas as pd
# from main_data import df

def getFlightRoutes(df):
    # This function gets the unique flight numbers and how often this flight number occurs in the original DataFrame
    # This is used for the drop-down menus
    instances = df.drop_duplicates(subset=['flightnr','date']).flightnr.value_counts().to_dict()
    # flight_routes_ = [(route, instances[flightnr]) for route, flightnr in zip(df['route'], df.drop_duplicates(subset=['flightnr'])['flightnr'])]
    flight_routes_ = [(route, instances[flightnr]) for route, flightnr in zip(df.drop_duplicates(subset=['route']).route, df.drop_duplicates(subset=['flightnr']).flightnr)]
    return(flight_routes_)

# def getOD(data):
#     # This function gets the unique OD-routes (without the stop-overs)
#     # This is used for the drop-down menus

def getHHMM(time):
    hours = int(time)
    minutes = int((time * 60) % 60)
    return(f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}')
