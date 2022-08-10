# This code is designed to implement the Mill's Apple Scab model on weather station data.
# https://www.canr.msu.edu/uploads/files/Research_Center/NW_Mich_Hort/Pests_IPM_Mgmt/Apple_Scab_1_Chart.pdf

#import software libraries
import pandas as pd
import numpy as np
import textwrap

#display all rows when printing the dataframe
pd.set_option('display.max_rows', None)

#read file
#file = r'C:\Users\ResononScanningSyst\Documents\GitHub\AutoMills\Stenvand\5Min_model\a11.csv'
file = r'C:\Users\ResononScanningSyst\Documents\GitHub\AutoMills\Stenvand\5Min_model\Mills_Table_data_reduced.csv'

df = pd.read_csv(file, sep = ',', parse_dates=['index'], usecols= ['index', 'rain', 'temp'])


#convert to datetime
df.index = pd.to_datetime(df.index)

#create duration column
df['duration'] = df['rain'].apply(lambda x: '0.0833333333333333' if x >= 90 else '')

#create rain_block column 
df['rain_block'] = (df['duration'].astype(bool).shift() != df['duration'].astype(bool)).cumsum()

#group by unique events map session and 5 minute rain increments back to dataframe
session_map = df[df['duration'].astype(bool)].groupby('rain_block')['rain_block'].nunique()
hour_map = df[df['duration'].astype(bool)].groupby('rain_block')['rain'].count()
df['sessions'] = df['rain_block'].map(session_map)
df['rain_5min'] = df['rain_block'].map(hour_map)

#create rain_hours column
df = df.groupby(['index','rain_block', 'rain_5min','temp', 'sessions'], as_index=False)['rain'].mean()
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

#create new column for index (infection dates:)
df['infection dates:']=df.groupby('rain_block').agg({'index': ['first']})

#drop rows with NaN values
df=df.dropna(axis=0)


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
df['lesion_result'] = df[['avg_temp', 'rain_hour_block']].apply(lambda x : mills_table(*x), axis=1)

df['lesion_result'] = df['lesion_result'].astype(int)


# replace any NaN data with empty string
df = df.replace(np.nan, '')

df['infection dates:'] = pd.to_datetime(df['infection dates:'])


# omit zero values in lesion_result column
df= df[df['lesion_result'] != 0]

# create temp variable to add days for 1 date
temp = df['lesion_result'].apply(np.ceil).apply(lambda x: pd.Timedelta(x, unit='D'))


#erase index colum for printing 
blankIndex=[''] * len(df)
df.index=blankIndex


# print Mills Table Results results
print('')
print('')
print('')
print('')
print('Mills Table Results:')
print('Stenvand et al. Model (1997)')
print('Last Revised: 5-01-03')
print('')
print('')
print(df[['infection dates:']])
print('')
print('')
value = """notes: The infection period is considered to start at the beginning of the rain. Symptoms, if the
infection is successful, will generally appear after 9 days incubation with average daily temperatures
at 60 F and after 16 days or more with average daily temperatures below 50F."""
  
# Wrap this text.
wrapper = textwrap.TextWrapper(width=100)
  
word_list = wrapper.wrap(text=value)
  
# Print each line.
for element in word_list:
    print(element)
print('')
print('')
print('')
print('')