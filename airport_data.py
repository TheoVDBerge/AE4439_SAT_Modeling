import pandas as pd
# Create a DataFrame from all IATA codes with relevant information, such as IATA code, name, and lat/lon data.
url = 'https://raw.githubusercontent.com/mborsetti/airportsdata/main/airportsdata/airports.csv'
df = pd.read_csv(url, index_col=0)

#%%

airports = ['FRA', 'ORD', 'LAX', 'JFK', 'BKK', 'SIN', 'ASB', 'HKG', 'BOM', 'DAC',
       'MAA', 'LEJ', 'TAS', 'IAH', 'YYZ', 'ATL', 'DFW', 'MEX', 'GDL',
       'UIO', 'DKR', 'VCP', 'EZE', 'MVD', 'CWB', 'SCL', 'CAI', 'JNB',
       'NBO', 'IST', 'TLV', 'BLR', 'HYD', 'DEL', 'KJA', 'NRT', 'SVO',
       'PEK', 'ICN', 'PVG', 'CKG', 'ALA', 'CAN', 'DMM', 'SHJ', 'RUH']

airport_data = {}

df_airport = df[df['iata'].isin(airports)]

# for i in airports:
#     airport_data[i] = {
#         'lat': df[df['iata'] == i]['lat'],
#         'lon': df[df['iata'] == i]['lon']
#         }