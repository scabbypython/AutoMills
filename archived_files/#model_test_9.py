#model_test_9

#import software libraries
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)

#read file
file = 'Mills_Table_data_reduced.csv'
#df = pd.read_csv(file, sep = ',', parse_dates=['index'], index_col=['index'],usecols= ['index', 'rain', 'temp'])
df = pd.read_csv(file, sep = ',', parse_dates=['index'], usecols= ['index', 'rain', 'temp'])


#convert to datetime
df.index = pd.to_datetime(df.index)

#create duration column
df['duration'] = df['rain'].apply(lambda x: '0.0833333333333333' if x >= 90 else '')

#create rain_block column 
df['rain_block'] = (df['duration'].astype(bool).shift() != df['duration'].astype(bool)).cumsum()

#create rain_hours column
session_map = df[df['duration'].astype(bool)].groupby('rain_block')['rain_block'].nunique()
hour_map = df[df['duration'].astype(bool)].groupby('rain_block')['rain'].count()
df['sessions'] = df['rain_block'].map(session_map)
df['rain_5min'] = df['rain_block'].map(hour_map)

df = df.groupby(['index','rain_block', 'rain_5min','temp', 'sessions'], as_index=False)['rain'].median()
df['rain_hours'] = df['rain_5min'] / df['sessions']/12

#calculate min temp of each rain_block
temp_results_min = df.groupby('rain_block').agg({'temp': ['min']})
df['temp_results_min']=temp_results_min

#calculate max temp of each rain_block
temp_results_max = df.groupby('rain_block').agg({'temp': ['max']})
df['temp_results_max']=temp_results_max

#calculate rain_hour_block
rain_hour_block = df.groupby('rain_block').agg({'rain_hours': ['mean']})
df['rain_hour_block']=rain_hour_block

#calculate average temp; (min+max)/2
df['avg_temp']=(df['temp_results_max'] + df['temp_results_min'])/2

#create new column for index (index2)
df['index2']=df.groupby('rain_block').agg({'index': ['first']})

#drop rows with NaN values
df=df.dropna(axis=0)


#define mills_table
def mills_table(avg_temp, rain_hour_block):
    #
    results = 0
    #
    if avg_temp >=43 and avg_temp <45:
        if rain_hour_block > 18:
            results = 'lesions in 17 days'
        else:
            results = ''
    elif avg_temp >=45 and avg_temp <46:
        if rain_hour_block > 15:
            results = 'lesions in 17 days'
        else:
            results = ''
    elif avg_temp >=46 and avg_temp <48:
        if rain_hour_block > 13:
            results = 'lesions in 17 days'
        else:
            results = ''
    elif avg_temp >=48 and avg_temp <50:
        if rain_hour_block > 12:
            results = 'lesions in 17 days'
        else:
            results = ''        
    elif avg_temp >=50 and avg_temp <52:
        if rain_hour_block > 11:
            results = 'lesions in 16 days'
        else:
            results = ''        
    elif avg_temp >=52 and avg_temp <54:
        if rain_hour_block > 9:
            results = 'lesions in 15 days'
        else:
            results = ''
    elif avg_temp >=54 and avg_temp <57:
        if rain_hour_block > 8:
            results = 'lesions in 14 days'
        else:
            results = ''        
    elif avg_temp >=57 and avg_temp <60:
        if rain_hour_block > 7:
            results = 'lesions in 11-13 days'
        else:
            results = ''        
    elif avg_temp >=60 and avg_temp <76:
        if rain_hour_block > 6:
            results = 'lesions in 9-10 days'
        else:
            results = ''        
            
            
            
    # returns results :)   
         
    return results        
            
# run the above mills_table function on the data      
df['lesion_result'] = df[['avg_temp', 'rain_hour_block']].apply(lambda x : mills_table(*x), axis=1)

# replace any NaN data with empty string
df = df.replace(np.nan, '')

# print dataframe results
print(df[['index2','rain_hour_block','avg_temp','lesion_result',]])