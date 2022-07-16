import pandas as pd
import numpy as np

file = 'Mills_Table.csv'
df = pd.read_csv(file, sep = ',', parse_dates= ['index'],encoding='utf-8-sig', usecols= ['index', 'rain', 'temp'],)    
df['duration'] = df['index'].dt.month

# create a new column for the duration
df['duration'] = df['rain'].apply(lambda x: '' if x <= 90 else '0.0833333333333333')


# create helper columns defining contiguous blocks and day
df['block'] = (df['duration'].astype(bool).shift() != df['duration'].astype(bool)).cumsum()
df['day'] = df['index'].dt.normalize()

# group by day to get unique block count and rain count
session_map = df[df['duration'].astype(bool)].groupby('day')['block'].nunique()
hour_map = df[df['duration'].astype(bool)].groupby('day')['rain'].count()

# map to original dataframe
df['sessions'] = df['day'].map(session_map)
df['rain(5min)'] = df['day'].map(hour_map)

# calculate dfult
df = df.groupby(['day', 'rain(5min)', 'temp', 'sessions'], as_index=False)['rain'].median()
df['rain(hours)'] = df['rain(5min)'] / df['sessions']/12


df['Event'] = df['rain(hours)'].apply(lambda x: 'infection' if x >= 6 else '')



# Mill's Table - need to compare temp column to the rain column
dfObj = pd.DataFrame(df, columns = ['day', 'rain(5min)', 'temp', 'sessions', 'rain', 'rain(hours)', 'Event', 'prognosis'])
df['prognosis'] = df['day'].map(hour_map)

prognosis = dfObj[(dfObj['temp'] > 43) & (dfObj['rain'] > 18) ]



df['prognosis'] = df['prognosis'].apply(lambda x: '' if x >= 1 else 'lesions in 17 days')
    
print("" , prognosis, sep='lesions in 17 days')


#print(df)

#     I think instead of days, it may be better to look at the whole thing as one continous time period and look at 
#     each individual "session (wetness period)" as a separate event to see if it is greater than 6 hours.
#     It may make more sense to ditch the polynomial and just code in the actual revised Mill's Table.

#     Mill's table derived from: https://extension.psu.edu/tree-fruit-disease-an-apple-scab-review