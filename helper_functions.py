import pandas as pd
from datetime import datetime
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

def getPayload(range_):
    
    range_ = range_ / 1.852
    
    def pounds2kg(lbs):
        return(lbs*0.45359237)
    
    # Takes range in km, returns payload in kg
    if range_ <= 3_890:
        return(pounds2kg(174_200))
    elif 3_900 < range_ <= 6_600:
        print('test')
        slope = (194_500 - 105_000)/(6_600 - 3_900)
        return(pounds2kg(194_500 - (slope)*(range_ - 3_900)))
    elif 6_600 < range_ <= 8_200:
        slope = (105_000 - 0)/(8_200 - 6_600)
        return(pounds2kg(105_000 - (slope)*(range_ - 6_600)))
    else:
        print('Out of range!')
        return(None)
