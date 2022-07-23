import pandas as pd
import numpy as np

# read in .csv file 'index' column should be date coumn

file = 'Mills_Table_data.csv'
df = pd.read_csv(file, sep = ',',parse_dates=['index'], index_col=['index'],usecols= ['index', 'rain', 'temp'])


# create a new column for the duration
df['duration'] = df['rain'].apply(lambda x: '' if x <= 90 else '0.0833333333333333')

# create helper columns defining contiguous blocks 
df['block'] = (df['duration'].astype(bool).shift() != df['duration'].astype(bool)).cumsum()



print(df)

###
unique_event = df[df['duration'].astype(bool)].groupby('block')['rain'].nunique()

print(unique_event)
# map to original df




results = df.groupby(unique_event).agg({['mean']})

print(results)


lesion_17 = df.loc[((results >= 43) & (results < 45)) & ((df[unique_event] > 18))] 
lesion_17 = df.loc[((df['temp'] >= 45) & (df['temp'] < 46)) & ((df[unique_event] > 15))]
lesion_17 = df.loc[((df['temp'] >= 46) & (df['temp'] < 48)) & ((df[unique_event] > 13))]
lesion_17 = df.loc[((df['temp'] >= 48) & (df['temp'] < 50)) & ((df[unique_event] > 12))]
lesion_16 = df.loc[((df['temp'] >= 50) & (df['temp'] < 52)) & ((df[unique_event] > 11))]
lesion_15 = df.loc[((df['temp'] >= 52) & (df['temp'] < 54)) & ((df[unique_event] >  9))]
lesion_14 = df.loc[((df['temp'] >= 54) & (df['temp'] < 57)) & ((df[unique_event] > 8))]
lesion_12_13 = df.loc[((df['temp'] >= 57) & (df['temp'] < 60)) & ((df[unique_event] > 7))]
lesion_9_10 = df.loc[((df['temp'] >= 60) & (df['temp'] < 76)) & ((df[unique_event] > 6))]



lesion_17.insert(6, "result", '17')
lesion_16.insert(6, "result", '16')
lesion_15.insert(6, "result", '15')
lesion_14.insert(6, "result", '14')
lesion_12_13.insert(6, "result", '12_13')
lesion_9_10.insert(6, "result", '9_10')

print(lesion_17, lesion_16, lesion_15, lesion_14, lesion_12_13, lesion_9_10)