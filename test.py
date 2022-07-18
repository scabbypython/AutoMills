import pandas as pd
import numpy as np

file = 'Mills_Table_data_short.csv'
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

#df = df[np.logical_and(df['temp'] >= 43, df['rain_hours'] > 18)]
result = df[((df['temp'] >=54) & (df['temp'] < 53)) & (df['rain_hours']) >= 1 & (df['rain_hours'] < 2)]

df['result'] = df['day'].map(hour_map)

print(df)


#df['Event'] = df['rain_hours'].apply(lambda x: 'infection' if x >= 6 else '')
 



# filter df




#print(df)
