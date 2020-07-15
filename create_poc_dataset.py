import pandas as pd
import numpy as np
from datetime import datetime, timedelta

dc_crashes = pd.read_csv('Crashes_in_DC.csv')
dc_crashes.REPORTDATE = pd.to_datetime(dc_crashes.REPORTDATE)
dc_2018 = dc_crashes[dc_crashes.REPORTDATE.dt.year == 2018]
dc_2018_bikes = dc_2018[dc_2018.TOTAL_BICYCLES > 0]

dc_final = dc_2018_bikes.groupby(by=dc_2018_bikes.REPORTDATE.dt.dayofyear).agg({'FATAL_BICYCLIST': ['sum'],
                                                                            'FATAL_PEDESTRIAN': ['sum'],
                                                                            'MAJORINJURIES_BICYCLIST': ['sum'],
                                                                            'MAJORINJURIES_PEDESTRIAN': ['sum'],
                                                                            'MINORINJURIES_BICYCLIST': ['sum'],
                                                                            'MINORINJURIES_PEDESTRIAN': ['sum'],
                                                                            'SPEEDING_INVOLVED': ['sum'],
                                                                            'TOTAL_VEHICLES': ['sum']
                                                                            })

capitalbikeshare = pd.read_csv('capitalbikeshare.csv')
capitalbikeshare['day by year'] = pd.to_datetime(capitalbikeshare['Start date'])
cb_usage = capitalbikeshare.groupby(by=capitalbikeshare['day by year'].dt.dayofyear).size()
cb_usage = pd.DataFrame(cb_usage)

df = cb_usage.merge(dc_final, left_index=True, right_index=True, how='outer')
df.columns = ['num_bikeshares',
              'fatalities_cyclists',
              'fatalities_pedestrians',
              'majorinjuries_cyclists',
              'majorinjuries_pedestrians',
              'minorinjuries_cyclists',
              'minorinjuries_pedestrians',
              'speeding', 'total_vehicles']

#weeks = np.tile(np.array([1, 2, 3, 4, 5, 6, 7]), 53)
#df['dayofweek'] = weeks[0:365]

start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 12, 31)
d = start_date
dates = [start_date]
while d < end_date:
    d += timedelta(days=1)
    dates.append(d)

df['dates'] = pd.to_datetime(dates)
df.to_csv('di_bike_safety_poc2.csv')

