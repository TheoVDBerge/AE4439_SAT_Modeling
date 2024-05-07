# ACLLP Felix Brandt visualization, data in YAML format

import yaml
import pandas as pd
import datetime
from datetime import date, time
import os
import matplotlib.pyplot as plt
import numpy as np
from airport_data import df_airport
from helper_functions import getPayload, getDistance

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

def flatten(input_):
    temp = []
    for lst in input_:
        if isinstance(lst, list):
            for nested_list in lst:
                temp.append(nested_list)
        else:
            temp.append()
    return(temp)

def arrangeAirports(flights):
    
    flight_map = {flight.split('-')[0]: flight.split('-')[1] for flight in flights}
    
    start = f'FRA-{flight_map["FRA"]}'
    
    result = [start]
    current_airport = start.split('-')[1]
    
    while len(result) < len(flights):
        next_airport = f'{current_airport}-{flight_map[current_airport]}'
        result.append(next_airport)
        current_location = flight_map[current_airport]
        
    return(result)

def getLeg(legs, airport):
    for i, idx in enumerate(legs):
        if airport in idx.split('-')[1]:
            return(idx)    

# test = data['flights']['LH8272-25NOV15-FRA-SCL']['legs'].keys()

def processData(data):
    maxPayloadMD11 = 90_000 # kg
    segments = list(data['segments'])
    # legs = list((data['flights'][list(data['flights'].keys())[0]]['legs']).keys())
    legs = [f'{i.split("-")[-2]}-{i.split("-")[-1]}' for i in data['flights'][list(data['flights'].keys())[0]]['legs'].keys()]
    time_ = unix2norm(data['flights'][list(data['flights'].keys())[0]]['std_timestamp'])
    for idy, j in enumerate(segments):
        for i in range(len((data['segments'][j]['shipments'].keys()))):
            shipmentnr = list(data['segments'][j]['shipments'].keys())[i]
            shipment = data['segments'][j]['shipments'][shipmentnr]['pieces'][f'{shipmentnr}x0']
            flightinfo = segments[idy].split('-')
            testshipments[f'{flightinfo[1]}-{flightinfo[0]}-{idy}-{i}'] = {
                'uniqueflightid': f'{flightinfo[0]}-{date2date2(time_)}',
                'shipmentnr': shipmentnr,
                'datetimeobject': time_, # This is dropped in the displayed table, but used for some charts
                'flightnr': flightinfo[0],
                'date': date2date2(time_),
                'std': date2time(time_),
                'origin': flightinfo[2],
                'dest': flightinfo[3],
                # 'route':flatten([[x.split('-')[2], x.split('-')[3]] for x in legs]),
                'route':[[x.split('-')[0], x.split('-')[1]] for x in legs],
                # 'route':[[x] for x in legs],
                # 'route': arrangeAirports(legs),
                'numpieces': shipment['amount'], # the amount of this item in each shipment
                'weight_1_item': shipment['weight'],
                'totalWeight': shipment['weight'] * shipment['amount'], 
                'leg': getLeg(legs,flightinfo[-1]), # This adds the actual leg (so from the airport prior to unloading to unloading airport). This will be useful later for getting the right payload
                'specials': shipment['specials'] if 'specials' in shipment.keys() else 0,
                'lf': round((shipment['weight'] * shipment['amount'])/maxPayloadMD11,4)} # Adjust this still for payload, maybe btter in app.py
    return()

# testdata = {'test':{'value1': 0,
#                     'value2': 'test',
#                     'value3': 100}
#             }    
testshipments = {}
datafiles = os.listdir('./base')
#%%

testfiles = ['LH8474-27NOV15-FRA-HKG.schedule.yaml', 'LH8044-28NOV15-FRA-ORD.schedule.yaml', 'LH8048-27NOV15-FRA-LAX.schedule.yaml']

for idx, i in enumerate(datafiles[39:50]):
# for idx, i in enumerate(testfiles[-1]):
    with open(f'./base/{i}', 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        processData(data)
        print(f'{i} completed! ({idx+1}/{len(datafiles)})')

# # Section to be commented out for PythonAnywhere
# testshipments = {}
# datafiles = os.listdir('/home/TheoVDBerge/mysite/base/')
# #%%

# testfiles = ['LH8474-27NOV15-FRA-HKG.schedule.yaml', 'LH8044-28NOV15-FRA-ORD.schedule.yaml', 'LH8048-27NOV15-FRA-LAX.schedule.yaml']

# for idx, i in enumerate(datafiles):
# # for idx, i in enumerate(testfiles[-1]):
#     with open(f'/home/TheoVDBerge/mysite/base/{i}', 'r') as f:
#         data = yaml.load(f, Loader=yaml.SafeLoader)
#         processData(data)
#         print(f'{i} completed! ({idx+1}/{len(datafiles)})')


df = pd.DataFrame.from_dict(testshipments, orient = 'index')
# print(df)

# A seeming discrepancy might seem that shipments on the same flight have different destinations, which is true because it consists of two legs! For example, LH8048, some shipments continue to LAX
# and others are off-loaded at ORD.

# #%% filter tests
# # print(df)
# # print()
# rslt_df = df[df['dest'] == 'ORD']
# # print(rslt_df)
# # print(rslt_df['totalWeight'].sum())
# # print()
# rslt_df2 = df[df['specials'].isin(['DGR'])]
# # rslt_df2 = df[df['specials'] == 'EAT PER PES']
# # print(rslt_df2)

# rslt_df3 = df.drop_duplicates(subset=['flightnr'])
# rslt_df4 = (df.drop_duplicates(subset=['flightnr', 'date']))
# occurences = rslt_df4['flightnr'].value_counts().reset_index().values.tolist()

# # print(rslt_df3)
# value_counts_dict = rslt_df4['flightnr'].value_counts().to_dict()

# rslt_df3['occurences'] = rslt_df3['flightnr'].map(value_counts_dict)

# flight_routes = (rslt_df3.loc[:,'route']).tolist()
# flight_routes2 = list(zip(rslt_df3['route'], rslt_df3['occurences']))
#%%

# testfilter = [x for x in df if df['']]

test2 = df['flightnr'].unique()

df2 = df[df['flightnr'] == test2[0]]


tempdata = []

for i in test2:
    temp = df[df['flightnr'] == i]
    temp2 = (temp['date'].unique())
    for j in temp2:
        tempdata.append(j)
    
# Plot test for number of flights per day
# keys, counts = np.unique(tempdata, return_counts=True)
# plt.bar(keys, counts)
# plt.xticks(rotation=45, ha="right")

# df['std'].value_counts(sort=False).plot.bar()


#TODO: Think about data I want to plot, what types of charts and UI for filtering
#TODO: Create rough lay-out on paper of the website 
# Check if a plotly file can be put in a container of Bootstrap?

#TODO: read all the flights in the folder and do some pivot table experiments first

#TODO: Check the different ULD types that are available?

