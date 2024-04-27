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

fig.write_html('./test2.html')
