# ACLLP Felix Brandt visualization, data in YAML format

import yaml
import pandas as pd
import datetime
from datetime import date
import os

#%%
def date2date(date_):
    return(date(2015, 11, int(date_[0:2])))

# Converts a datetime object to a YYYY-MM-DD
def date2date2(date_):
    return(date_.strftime('%Y-%m-%d'))

# Convert a datetime object to HH:MM
def date2time(date_):
    return(date_.strftime('%H:%M'))

# Convert a Epoch time (Unix time) to a datetime object
def unix2norm(timestamp):
    return(datetime.datetime.fromtimestamp(timestamp))

# Flattens a list of nested lists
def flatten(input_):
    temp = []
    for lst in input_:
        if isinstance(lst, list):
            for nested_list in lst:
                temp.append(nested_list)
        else:
            temp.append()
    return(temp)

# Puts the legs in the correct order
def arrangeAirports(flights):
    
    flight_map = {flight.split('-')[0]: flight.split('-')[1] for flight in flights}
    
    start = f'FRA-{flight_map["FRA"]}'
    
    result = [start]
    current_airport = start.split('-')[1]
    
    while len(result) < len(flights):
        next_airport = f'{current_airport}-{flight_map[current_airport]}'
        result.append(next_airport)
        current_airport = flight_map[current_airport]
        
    return(result)

# Gets the legs from a certain flights
def getLeg(legs, airport):
    for i, idx in enumerate(legs):
        if airport in idx.split('-')[1]:
            return(idx)    

# Process the raw data into a dictionary
def processData(data):
    maxPayloadMD11 = 90_000 # kg
    segments = list(data['segments'])
    legs = [f'{i.split("-")[-2]}-{i.split("-")[-1]}' for i in data['flights'][list(data['flights'].keys())[0]]['legs'].keys()]
    time_ = unix2norm(data['flights'][list(data['flights'].keys())[0]]['std_timestamp'])
    for idy, j in enumerate(segments):
        for i in range(len((data['segments'][j]['shipments'].keys()))):
            shipmentnr = list(data['segments'][j]['shipments'].keys())[i]
            shipment = data['segments'][j]['shipments'][shipmentnr]['pieces'][f'{shipmentnr}x0']
            flightinfo = segments[idy].split('-')
            shipments[f'{flightinfo[1]}-{flightinfo[0]}-{idy}-{i}'] = {
                'uniqueflightid': f'{flightinfo[0]}-{date2date2(time_)}',
                'shipmentnr': shipmentnr,
                'datetimeobject': time_, # This is dropped in the displayed table, but used for some charts
                'flightnr': flightinfo[0],
                'date': date2date2(time_),
                'std': date2time(time_),
                'origin': flightinfo[2],
                'dest': flightinfo[3],
                'route':[[x.split('-')[0], x.split('-')[1]] for x in legs],
                'numpieces': shipment['amount'], # the amount of this item in each shipment
                'weight_1_item': shipment['weight'],
                'totalWeight': shipment['weight'] * shipment['amount'], 
                'leg': getLeg(legs,flightinfo[-1]), # This adds the actual leg (so from the airport prior to unloading to unloading airport). This will be useful later for getting the right payload
                'specials': shipment['specials'] if 'specials' in shipment.keys() else 0,
                'lf': round((shipment['weight'] * shipment['amount'])/maxPayloadMD11,4)}
    return()

# Initialize the DataFrame
shipments = {}

# Generate a list of all the raw YAML files

# To be un-commented for local Python
datafiles = os.listdir('./base')

# To be un-commented for PythonAnywhere
# datafiles = os.listdir('/home/TheoVDBerge/mysite/base/')

for idx, i in enumerate(datafiles):
    with open(f'./base/{i}', 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        processData(data)
        print(f'{i} completed! ({idx+1}/{len(datafiles)})')

# Convert dictionary to Pandas DataFrame
df = pd.DataFrame.from_dict(shipments, orient = 'index')
