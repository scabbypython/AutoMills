#     This file sorts out days with leaf wetness events over 90% (rain(5min)), it counts those 5 minute periods 
#     and seperates out how many discrete one there are per day (how many times it started and stopped). The 
#     "value" given is the median wetness sensor reading per day. The rain(hours) is the total rain period per day.
#     The data file used to test this with correct headings is rain_events.csv

# import our file, make sure file name and tabs match
import pandas as pd
file = 'rain_events.csv'
df = pd.read_csv(file, sep = ',', parse_dates= ['index'],encoding='utf-8-sig', usecols= ['index', 'value'],)    
df['duration'] = df['index'].dt.month

# create a new column for the duration
df['duration'] = df['value'].apply(lambda x: '' if x <= 90 else '0.0833333333333333')


# create helper columns defining contiguous blocks and day
df['block'] = (df['duration'].astype(bool).shift() != df['duration'].astype(bool)).cumsum()
df['day'] = df['index'].dt.normalize()

# group by day to get unique block count and value count
session_map = df[df['duration'].astype(bool)].groupby('day')['block'].nunique()
hour_map = df[df['duration'].astype(bool)].groupby('day')['value'].count()

# map to original dataframe
df['sessions'] = df['day'].map(session_map)
df['rain(5min)'] = df['day'].map(hour_map)

# calculate result
res = df.groupby(['day', 'rain(5min)', 'sessions'], as_index=False)['value'].median()
res['rain(hours)'] = res['rain(5min)'] / res['sessions']/12
#res['amount'] = res['value'] / res['sessions']

print(res)