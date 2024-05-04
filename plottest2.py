import plotly.graph_objects as go
from main_data import df

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


fig.write_html('./test2.html')
