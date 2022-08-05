# This code is designed to implement the Mill's Apple Scab model on weather station data.
# https://www.canr.msu.edu/uploads/files/Research_Center/NW_Mich_Hort/Pests_IPM_Mgmt/Apple_Scab_1_Chart.pdf

#import software libraries
import pandas as pd
import numpy as np

#display all rows when printing the dataframe
#pd.set_option('display.max_rows', None)
file = r'C:\Users\proco\Documents\GitHub\AutoMills\Stenvand\5Min_model\a11_merged.csv'
df = pd.read_csv(file, parse_dates=['index'], index_col=['index'],usecols= ['index', 'rain', 'temp'])

df['index'] = pd.to_datetime(df['index'])

# resample 5 minute data to hourly data using mean

df2 = df.resample('H').mean()

#df_hour_sum = df.resample('H').sum()


print(df2)
#convert to datetime
#df.index = pd.to_datetime(df.index)
#df = df.set_index(pd.to_datetime(df.index))
#df = df.set_index('index') 
#df.resample('H').mean()

#print(df)
#create duration column
df2['duration'] = df['rain'].apply(lambda x: '1' if x >= 90 else '')

#create rain_block column 
df2['rain_block'] = (df2['duration'].astype(bool).shift() != df2['duration'].astype(bool)).cumsum()

#group by unique events map session and 5 minute rain increments back to dataframe
session_map = df2[df2['duration'].astype(bool)].groupby('rain_block')['rain_block'].nunique()
hour_map = df2[df2['duration'].astype(bool)].groupby('rain_block')['rain'].count()
df2['sessions'] = df2['rain_block'].map(session_map)
#changed rain_5min to rain_60min
df2['rain_60min'] = df2['rain_block'].map(hour_map)

#create rain_hours column
df2 = df2.groupby(['index','rain_block', 'rain_60min','temp', 'sessions'], as_index=False)['rain'].median()
#no longer divide by 12 to get rain_hours, because it is already in 60 min intervals
df2['rain_hours'] = df2['rain_60min'] / df2['sessions']

#calculate min temp of each rain_block
temp_results_min = df2.groupby('rain_block').agg({'temp': ['min']})
df2['temp_results_min']=temp_results_min

#calculate max temp of each rain_block
temp_results_max = df2.groupby('rain_block').agg({'temp': ['max']})
df2['temp_results_max']=temp_results_max

#calculate rain_hour_block
rain_hour_block = df2.groupby('rain_block').agg({'rain_hours': ['mean']})
df2['rain_hour_block']=rain_hour_block

#calculate average temp; (min+max)/2
df2['avg_temp']=(df2['temp_results_max'] + df2['temp_results_min'])/2


#create new column for index (index2)
df2['index2']=df2.groupby('rain_block').agg({'index': ['first']})

#drop rows with NaN values
df2=df2.dropna(axis=0)


#define mills_table function
def mills_table(avg_temp, rain_hour_block):
    #
    results = 0
    #
    if avg_temp >=34 and avg_temp <36:
        if rain_hour_block > 41:
            results = '1'
        else:
            results = '0'
    elif avg_temp >=36 and avg_temp <37:
        if rain_hour_block > 35:
            results = '1'
        else:
            results = '0'
    elif avg_temp >=37 and avg_temp <39:
        if rain_hour_block > 30:
            results = '1'
        else:
            results = '0'
    elif avg_temp >=39 and avg_temp <41:
        if rain_hour_block > 28:
            results = '1'
        else:
            results = '0'        
    elif avg_temp >=41 and avg_temp <43:
        if rain_hour_block > 21:
            results = '1'
        else:
            results = '0'        
    elif avg_temp >=43 and avg_temp <45:
        if rain_hour_block > 18:
            results = '1'
        else:
            results = '0'
    elif avg_temp >=45 and avg_temp <46:
        if rain_hour_block > 15:
            results = '1'
        else:
            results = '0'        
    elif avg_temp >=46 and avg_temp <48:
        if rain_hour_block > 13:
            results = '1'
        else:
            results = '0'        
    elif avg_temp >=48 and avg_temp <50:
        if rain_hour_block > 12:
            results = '1'
        else:
            results = '0'    
    elif avg_temp >=50 and avg_temp <52:
        if rain_hour_block > 11:
            results = '1'
        else:
            results = '0'  
    elif avg_temp >=52 and avg_temp <54:
        if rain_hour_block > 9:
            results = '1'
        else:
            results = '0' 
    elif avg_temp >=54 and avg_temp <55:
        if rain_hour_block > 8:
            results = '1'
        else:
            results = '0' 
    elif avg_temp >=55 and avg_temp <57:
        if rain_hour_block > 8:
            results = '1'
        else:
            results = '0'             
    elif avg_temp >=57 and avg_temp <59:
        if rain_hour_block > 7:
            results = '1'
        else:
            results = '0' 
    elif avg_temp >=59 and avg_temp <61:
        if rain_hour_block > 7:
            results = '1'
        else:
            results = '0'                                         
    elif avg_temp >=61 and avg_temp <77:
        if rain_hour_block > 6:
            results = '1'
        else:
            results = '0'   
    elif avg_temp >=77 and avg_temp <150:
        if rain_hour_block > 8:
            results = '1'
        else:
            results = '0'     
                     
    return results        
            
# run the mills_table function on the data      
df2['lesion_result'] = df2[['avg_temp', 'rain_hour_block']].apply(lambda x : mills_table(*x), axis=1)

df2['lesion_result'] = df2['lesion_result'].astype(int)


# replace any NaN data with empty string
df2 = df2.replace(np.nan, '')

df2['index2'] = pd.to_datetime(df['index2'])


# omit zero values in lesion_result column
df2= df2[df2['lesion_result'] != 0]


#erase index colum for printing 
blankIndex=[''] * len(df2)
df2.index=blankIndex


# print Mills Table Results results
print('')
print('')
print('Mills Table Results:')
print('')
print('')

print(df[['index2']])
