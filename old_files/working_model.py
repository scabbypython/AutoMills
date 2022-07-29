# this is my latest attempt, it seems to be doing something without errors...

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




# replace all NaN with 0 - may not be needed

df = df.replace(np.nan, 0)


# create function to calculate mills table

def mills_table(temp, rain_block):
    #
    results = 0
    #
    if temp >=43 and temp <45:
        if rain_block > 18:
            results = 'lesions in 17 days'
        else:
            results = ''
    elif temp >=45 and temp <46:
        if rain_block > 15:
            results = 'lesions in 17 days'
        else:
            results = ''
    elif temp >=46 and temp <48:
        if rain_block > 13:
            results = 'lesions in 17 days'
        else:
            results = ''
    elif temp >=48 and temp <50:
        if rain_block > 12:
            results = 'lesions in 17 days'
        else:
            results = ''        
    elif temp >=50 and temp <52:
        if rain_block > 11:
            results = 'lesions in 16 days'
        else:
            results = ''        
    elif temp >=52 and temp <54:
        if rain_block > 9:
            results = 'lesions in 15 days'
        else:
            results = ''
    elif temp >=54 and temp <57:
        if rain_block > 8:
            results = 'lesions in 14 days'
        else:
            results = ''        
    elif temp >=57 and temp <60:
        if rain_block > 7:
            results = 'lesions in 11-13 days'
        else:
            results = ''        
    elif temp >=60 and temp <76:
        if rain_block > 6:
            results = 'lesions in 9-10 days'
        else:
            results = ''        
            
            
            
    # returns results :)        
    return results        
            
            
# run the above mills_table function on the data
            
df["lesion result"] = df[["temp", "rain_block"]].apply(lambda x : mills_table(*x), axis=1)


# replace any NaN data with empty string

df = df.replace(np.nan, '')

# print dataframe results

print(df["lesion result"])

