import pandas as pd

data = {
    'Tuesday': {'LH8290 (FRA-CAI)': 0.56, 'LH8340 (FRA-TLV)': 0.39, 'LH8340 (TLV-IST)': 0.27},
    'Wednesday': {'LH8272 (FRA-DKR)': 0.07, 'LH8272 (DKR-VCP)': 0.05, 'LH8272 (VCP-CWB)': 0.02, 'LH8272 (CWB-SCL)': 0.01, 'LH8364 (FRA-BLR)': 0.17, 'LH8364 (BLR-HYD)': 0.14},
    'Thursday': {'LH8290 (FRA-CAI)': 0.57, 'LH8340 (FRA-TLV)': 0.73, 'LH8340 (TLV-IST)': 0.42},
    'Friday': {'LH8296 (FRA-NBO)': 0.65, 'LH8296 (NBO-JNB)': 0.43},
    'Saturday': {'LH8340 (FRA-TLV)': 0.31, 'LH8340 (TLV-IST)': 0.23, 'LH8364 (FRA-BLR)': 0.54, 'LH8364 (BLR-HYD)': 0.35},
    'Sunday': {'LH8290 (FRA-CAI)': 0.67, 'LH8340 (FRA-TLV)': 0.71, 'LH8340 (TLV-IST)': 0.41}
}

# Initialize lists to store data
days = []
flights = []
load_factors = []

# Iterate over the dictionary to populate the lists
for day, flights_info in data.items():
    for flight_leg, load_factor in flights_info.items():
        days.append(day)
        flights.append(flight_leg)
        load_factors.append(load_factor)

# Create DataFrame
df = pd.DataFrame({
    'Day': days,
    'FlightLeg': flights,
    'LoadFactor': load_factors
})

# Split the FlightLeg into FlightNumber and Leg
df[['FlightNumber', 'Leg']] = df['FlightLeg'].str.extract(r'(^LH\d+) \((.+)\)')
df.drop(columns=['FlightLeg'], inplace=True)

# Preview the DataFrame
# print(df.head())


import plotly.express as px

fig = px.bar(df, x='FlightNumber', y='LoadFactor', color='Day',
             hover_data=['Leg'], barmode='stack',
             title="Load Factor by Flight Number Across Different Days",
             labels={"LoadFactor": "Load Factor", "FlightNumber": "Flight Number"})

fig.update_layout(xaxis={'categoryorder':'total descending'},
                  yaxis_title="Load Factor",
                  legend_title="Day")

fig.write_html('./test7.html')