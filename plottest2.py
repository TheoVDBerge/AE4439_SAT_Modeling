import plotly.graph_objects as go
from main_data import df
from helper_functions import getDistance, getPayload

#%%

from datetime import datetime

def getDayOfWeek(date_string):
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    
    # Get the day of the week as an integer
    day_of_week_index = date_obj.weekday()
    
    # List of days, could be defined outside the function if used frequently to avoid redefinition
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Get the day of the week name from the list
    day_of_week_name = days_of_week[day_of_week_index]
    
    # Return both the numeric index and the name of the day of the week
    return (day_of_week_index, day_of_week_name)

flightnumbers = df.flightnr.unique()

valtest = df.groupby(['date', 'flightnr'])['lf'].sum()

unique_dates = valtest.index.get_level_values('date').unique()
unique_flightnr = valtest.index.get_level_values('flightnr').unique()

daily_data = []

for flight in unique_dates:
    temp = []
    for date in unique_flightnr:
        try:
            temp.append(valtest[flight][date])
        except:
            temp.append(0)
    
    daily_data.append(temp)
    
days = [x for x in range(0,7)]

final_data = {getDayOfWeek(unique_dates[i])[1]: daily_data[i] for i in range(len(unique_dates))}
    
# Create a figure object
fig = go.Figure()


# Loop through the zoos_data dictionary to create a bar for each zoo
for day, values in final_data.items():
    fig.add_trace(go.Bar(name=day, x=unique_flightnr, y=values))

fig.update_layout(barmode='stack')

#%%
import plotly.express as px

depdata = df.drop_duplicates('uniqueflightid')['datetimeobject']

type_ = 'hourly'

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
    
# elif type_ == 'hourly':
    
#     # deptimes = [f'{x}:00' for x in range(0,25)]
    
#     xlabel_ = 'Time'
#     ylabel_ = 'Occurences'
#     range_ = [0,25]
#     n_bins = 25
    
#     x_data = [0] * len(depdata)

#     for i, time_ in enumerate(depdata):
#         x_data[i] = time_.hour

elif type_ == 'hourly':
    
    deptimes = [f'{x}:00' for x in range(0,25)]
    
    xlabel_ = 'Time'
    ylabel_ = 'Occurences'
    range_ = [0,25]
    n_bins = 25
    
    depcat = [0] * 25
    for time in depdata:
        time_ = time.hour
        depcat[time_] += 1
        
fig = px.histogram(x = deptimes,
                   y = depcat,
                   nbins = n_bins,
                   color_discrete_sequence=["#ffb500"])

# fig.update_yaxes(ticklabelstep=2)
fig.update_layout(
   title={'text': 'test', 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'},
   xaxis_tickangle = -45,
   bargap = 0.1,
   yaxis_title = ylabel_,
   xaxis_title = xlabel_,
   xaxis_range = range_,
   template = 'plotly_dark'
)

# fig = px.histogram(x_data, nbins = 25)
#%%

import plotly.graph_objects as go

# Assuming `final_data` and `unique_flightnr` are defined
# Let's also assume you have `flight_descriptions` which is a dictionary with additional info

flight_descriptions = {
    "Flight1": "Info about Flight1",
    "Flight2": "Info about Flight2",
    "Flight3": "Info about Flight3",
    # Add more descriptions as necessary
}

fig = go.Figure()

for day, values in final_data.items():
    # Prepare hover text for each bar
    hover_texts = [f"{fnr}: {flight_descriptions.get(fnr, 'No description available')}" for fnr in unique_flightnr]
    # Add trace with hover text
    fig.add_trace(
        go.Bar(
            name=day,
            x=unique_flightnr,
            y=values,
            hovertext=hover_texts,
            hoverinfo='text+y'  # Shows the hover text along with the y-values
        )
    )

# Update layout if necessary
fig.update_layout(
    title="Flight Data by Day",
    xaxis_title="Flight Number",
    yaxis_title="Some Metric",
    barmode='stack'
)
print(final_data)

#%%
from main_data import df

# sorted_data = df.groupby(['date', 'flightnr'])['lf'].sum()
sorted_data = df.groupby(['date', 'flightnr', 'leg'])['totalWeight'].sum()

# Due to the double indexing, I extract the unique values of 
# both levels of indexes.
unique_dates = sorted_data.index.get_level_values('date').unique()
unique_flightnr = sorted_data.index.get_level_values('flightnr').unique()
unique_legs = sorted_data.index.get_level_values('leg').unique()


test = {}

from main_data import arrangeAirports

import pandas as pd

# daily_data = []

# for day in unique_dates:
#     temp = []
#     weekday = getDayOfWeek(day)[1]
    
#     for flight_ in sorted_data[day].index.get_level_values('flightnr').unique():
#         temp2 = []
#         for leg in arrangeAirports(sorted_data[day][flight_].index.get_level_values('leg')):
#             test[weekday]: {flight_, leg} = 1
            
            
# testdata = {getDayOfWeek(day)[1]:{{f'{flight} ({leg})': 1}
#                                   for flight in sorted_data[day].index.get_level_values('flightnr').unique() for leg in sorted_data[day][flight].index.get_level_values('leg')}
#             for day in unique_dates }



from airport_data import df_airport

days2 = []
flightnr2 = []
leg2 = []
load_factors2 = []

for day2 in unique_dates:
    for flight in sorted_data[day2].index.get_level_values('flightnr').unique():
        for num, leg in enumerate(arrangeAirports(sorted_data[day2].loc[flight].index.get_level_values('leg'))):
            days2.append(getDayOfWeek(day2)[1])
            flightnr2.append(flight)
            leg2.append(leg)
            load_factors2.append(round((sorted_data[day2][flight].iloc[num:].sum())/getPayload(getDistance(df_airport, leg)), 2))
            
df22 = pd.DataFrame({
    'Day': days2,
    'flightnr': flightnr2,
    'leg': leg2,
    'LoadFactor': load_factors2
})
    


#%%

data = {
    getDayOfWeek(day)[1]: {
        f'{flight} ({leg})': round((sorted_data[day][flight].iloc[num:].sum())/getPayload(getDistance(df_airport, leg)), 2)
        for flight in sorted_data[day].index.get_level_values('flightnr').unique()
        for num, leg in enumerate(arrangeAirports(sorted_data[day].loc[flight].index.get_level_values('leg'))) # Arrange the airports in chronological order to ensure the load factor per leg can be calculated more easily
    }
    for day in unique_dates
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
df2 = pd.DataFrame({
    'Day': days,
    'FlightLeg': flights,
    'LoadFactor': load_factors
})



# Split the FlightLeg into FlightNumber and Leg
df2[['FlightNumber', 'Leg']] = df2['FlightLeg'].str.extract(r'(^LH\d+) \((.+)\)')
df2.drop(columns=['FlightLeg'], inplace=True)

# Preview the DataFrame
# print(df.head())


import plotly.express as px

fig = px.bar(df2, x='FlightNumber', y='LoadFactor', color='Day',
             hover_data=['Leg'], barmode='stack',
             title="Load Factor by Flight Number Across Different Days",
             labels={"FlightNumber": "Flight number", "LoadFactor": "Load factor"},
             )

fig.update_layout(xaxis={'categoryorder':'total descending'},
                  yaxis_title="Load Factor",
                  legend_title="Day",
                  xaxis_tickangle = -45,
                  template = 'plotly_dark')

fig.write_html('./test7.html')

#TODO: maybe add dictionary type with day: {flightnr: {flightnr: lf, flightr2: lf2}}

    
# final_data = {getDayOfWeek(unique_dates[i])[1]: daily_data[i] for i in range(len(unique_dates))}

 #%%   
 
import plotly.graph_objects as go

# Sample data
categories = ['LH8290', 'LH8340', 'LH8272']
days = ['Leg 1', 'Leg 2']
values_primary = [10, 20, 30]
values_secondary = [5, 10, 15]
nested_values = [2, 4, 6]

fig = go.Figure()

# Add the primary metric trace
for i, day in enumerate(days):
    fig.add_trace(
        go.Bar(
            name=f'Primary-{day}',
            x=categories,
            y=[v + i * 35 for v in values_primary],  # Adding some offset for illustration
            offsetgroup=i,
            text=values_primary,
            hoverinfo='text+name'
        )
    )

    # Add the secondary metric trace
    fig.add_trace(
        go.Bar(
            name=f'Secondary-{day}',
            x=categories,
            y=[v + i * 35 for v in values_secondary],
            offsetgroup=i,
            base=[v + i * 35 for v in values_primary],
            text=values_secondary,
            hoverinfo='text+name',
            showlegend = False
        )
    )
    


# Update the layout
fig.update_layout(
    barmode='group',
    title='Nested Stacked Bar Chart',
    xaxis_title='Category',
    yaxis_title='Values',
    legend_title='Metric',
)

# fig.show()


fig.write_html('./test4.html')
#%%

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Create dummy data indexed by month and with multi-columns [product, revenue]
index = ["California", "Texas", "Arizona", "Nevada", "Louisiana"]
df = pd.concat(
    [
        pd.DataFrame(
            np.random.rand(5, 3) * 1.25 + 0.25,
            index=index,
            columns=["Revenue1", "Revenue2", "Revenue3"]
        ),
        pd.DataFrame(
            np.random.rand(5, 3) + 0.5,
            index=index,
            columns=["Revenue1", "Revenue2", "Revenue3"]
        ),
    ],
    axis=1,
    keys=["Product1", "Product2"]
)

# Create a figure with the right layout
fig = go.Figure(
    layout=go.Layout(
        height=600,
        width=1000,
        barmode="relative",
        yaxis_showticklabels=False,
        yaxis_showgrid=False,
        yaxis_range=[0, df.groupby(axis=1, level=0).sum().max().max() * 1.5],
       # Secondary y-axis overlayed on the primary one and not visible
        yaxis2=go.layout.YAxis(
            visible=False,
            matches="y",
            overlaying="y",
            anchor="x",
        ),
        font=dict(size=24),
        legend_x=0,
        legend_y=1,
        legend_orientation="h",
        hovermode="x",
        margin=dict(b=0,t=10,l=0,r=10)
    )
)

# Define some colors for the product, revenue pairs
colors = {
    "Product1": {
        "Revenue1": "#F28F1D",
        "Revenue2": "#F6C619",
        "Revenue3": "#FADD75",
    },
    "Product2": {
        "Revenue1": "#2B6045",
        "Revenue2": "#5EB88A",
        "Revenue3": "#9ED4B9",
    }
}

# Add the traces
for i, t in enumerate(colors):
    for j, col in enumerate(df[t].columns):
        if (df[t][col] == 0).all():
            continue
        fig.add_bar(
            x=df.index,
            y=df[t][col],
            # Set the right yaxis depending on the selected product (from enumerate)
            yaxis=f"y{i + 1}",
            # Offset the bar trace, offset needs to match the width
            # For categorical traces, each category is spaced by 1
            offsetgroup=str(i),
            offset=(i - 1) * 1/3,
            width=1/3,
            legendgroup=t,
            legendgrouptitle_text=t,
            name=col,
            marker_color=colors[t][col],
            marker_line=dict(width=2, color="#333"),
            hovertemplate="%{y}<extra></extra>"
        )

fig.write_html('./test5.html')

#%%

import pandas as pd

data = pd.DataFrame(
    dict(
        year=[*[2000, 2010, 2020]*4],
        var=[*[10, 20, 15], *[12, 8, 18], *[10, 17, 13], *[12, 11, 20]],
        names=[
            *["spent on fruit"]*3,
            *["spent on toys"]*3,
            *["earned from stocks"]*3,
            *["earned from gambling"]*3,
        ],
        groups=[*["subgroup1"]*6, *["subgroup2"]*6]
    )
)

import plotly.express as px

fig = px.bar(data, x="groups", y="var", facet_col="year", color="names")
fig.write_html('./test6.html')

#%% Create a figure object
fig = go.Figure()

# Loop through the final_data to create a bar for each day of the week
for day, values in final_data.items():
    fig.add_trace(go.Bar(name=day, x=unique_flightnr, y=values))

fig.update_layout(barmode='stack')

fig.write_html('./test3.html')
