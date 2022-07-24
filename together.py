# This code seems to print the correct infection periods, it currently prints out the whole df though


import pandas as pd
import numpy as np

# read in .csv file 'index' column should be date 

file = 'Mills_Table_data.csv'
df = pd.read_csv(file, sep = ',',parse_dates=['index'], index_col=['index'],usecols= ['index', 'rain', 'temp'])


# create a new column for 'rain_event'; if the 'rain' reading is greater or equal to 90 print '0.0833333333333333' 
# (minutes or 1/12 of an hour) else print nothing

df['rain_event'] = df['rain'].apply(lambda x: '0.0833333333333333' if x >= 90 else '')


# Create a new column for 'rain_block'; this keeps a cumulative sum of rain events

df['rain_block'] = (df['rain_event'].astype(bool).shift() != df['rain_event'].astype(bool)).cumsum()



# group by unique rain blocks

rain_block_map = df[df['rain_event'].astype(bool)].groupby('rain_block')['rain_event'].nunique()




# map to original df

df['rain_block_hour'] = df['rain_block'].map(rain_block_map)




# replace all NaN with 0

df = df.replace(np.nan, 0)



# print dataframe

#print(df)



lesion_17_1 = df.loc[((df['temp'] >= 43) & (df['temp'] < 45)) & ((df['rain_block'] > 18))] 
lesion_17_2 = df.loc[((df['temp'] >= 45) & (df['temp'] < 46)) & ((df['rain_block'] > 15))]
lesion_17_3 = df.loc[((df['temp'] >= 46) & (df['temp'] < 48)) & ((df['rain_block'] > 13))]
lesion_17_4 = df.loc[((df['temp'] >= 48) & (df['temp'] < 50)) & ((df['rain_block'] > 12))]
lesion_16 = df.loc[((df['temp'] >= 50) & (df['temp'] < 52)) & ((df['rain_block'] > 11))]
lesion_15 = df.loc[((df['temp'] >= 52) & (df['temp'] < 54)) & ((df['rain_block'] >  9))]
lesion_14 = df.loc[((df['temp'] >= 54) & (df['temp'] < 57)) & ((df['rain_block'] > 8))]
lesion_11_13 = df.loc[((df['temp'] >= 57) & (df['temp'] < 60)) & ((df['rain_block'] > 7))]
lesion_9_10 = df.loc[((df['temp'] >= 60) & (df['temp'] < 76)) & ((df['rain_block'] > 6))]





df['infection_event'] = df['rain_block'].apply(lambda x: '17 days' if x >= 12 else '')
df['infection_event'] = df['rain_block'].apply(lambda x: '16 days' if x >= 11 else '')
df['infection_event'] = df['rain_block'].apply(lambda x: '15 days' if x >= 9 else '')
df['infection_event'] = df['rain_block'].apply(lambda x: '14days' if x >= 8 else '')
df['infection_event'] = df['rain_block'].apply(lambda x: '11-13 days' if x >= 7 else '')
df['infection_event'] = df['rain_block'].apply(lambda x: '9-10 days' if x >= 6 else '')

print(df['infection_event'])

#print(df['infection_event'].to_string())



#print(lesion_9_10['rain_block'])
#print(lesion_11_13['rain_block'])
#print(lesion_14['rain_block'])
#print(lesion_15['rain_block'])
#print(lesion_16['rain_block'])
#print(lesion_17_1['rain_block'])
#print(lesion_17_2['rain_block'])
#rint(lesion_17_3['rain_block'])
#print(lesion_17_4['rain_block'])



#print (df['infection_event'])


#lesion_17_1.insert(1, "result", '17')
#lesion_17_2.insert(1, "result", '17')
#lesion_17_3.insert(1, "result", '17')
#lesion_17_4.insert(1, "result", '17')
#lesion_16.insert(1, "result", '16')
#lesion_15.insert(1, "result", '15')
#lesion_14.insert(1, "result", '14')
#lesion_11_13.insert(1, "result", '12_13')
#lesion_9_10.insert(1, "result", '9_10')


#print(lesion_17_1, lesion_17_2, lesion_17_3, lesion_17_4, lesion_16, lesion_15, lesion_14, lesion_12_13, lesion_9_10)