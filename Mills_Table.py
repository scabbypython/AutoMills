import pandas as pd
import numpy as np

file = 'Mills_Table_data.csv'
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

# map to original df
df['sessions'] = df['day'].map(session_map)
df['rain_5min'] = df['day'].map(hour_map)

# calculate dfult
df = df.groupby(['day', 'rain_5min', 'temp', 'sessions'], as_index=False)['rain'].median()
df['rain_hours'] = df['rain_5min'] / df['sessions']/12


lesion_17 = df.loc[((df['temp'] >= 43) & (df['temp'] < 45)) & ((df['rain_hours'] > 18))] 
lesion_17 = df.loc[((df['temp'] >= 45) & (df['temp'] < 46)) & ((df['rain_hours'] > 15))]
lesion_17 = df.loc[((df['temp'] >= 46) & (df['temp'] < 48)) & ((df['rain_hours'] > 13))]
lesion_17 = df.loc[((df['temp'] >= 48) & (df['temp'] < 50)) & ((df['rain_hours'] > 12))]
lesion_16 = df.loc[((df['temp'] >= 50) & (df['temp'] < 52)) & ((df['rain_hours'] > 11))]
lesion_15 = df.loc[((df['temp'] >= 52) & (df['temp'] < 54)) & ((df['rain_hours'] >  9))]
lesion_14 = df.loc[((df['temp'] >= 54) & (df['temp'] < 57)) & ((df['rain_hours'] > 8))]
lesion_12_13 = df.loc[((df['temp'] >= 57) & (df['temp'] < 60)) & ((df['rain_hours'] > 7))]
lesion_9_10 = df.loc[((df['temp'] >= 60) & (df['temp'] < 76)) & ((df['rain_hours'] > 6))]



lesion_17.insert(6, "result", '17')
lesion_16.insert(6, "result", '16')
lesion_15.insert(6, "result", '15')
lesion_14.insert(6, "result", '14')
lesion_12_13.insert(6, "result", '12_13')
lesion_9_10.insert(6, "result", '9_10')

print(lesion_17, lesion_16, lesion_15, lesion_14, lesion_12_13, lesion_9_10)




#     Mill's table derived from: https://extension.psu.edu/tree-fruit-disease-an-apple-scab-review