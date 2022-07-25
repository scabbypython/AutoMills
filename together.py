# this is my latest attempt, it seems to be doing something without errors...

import pandas as pd
import numpy as np

# read in .csv file 'index' column should be date 

file = 'Mills_Table_data_reduced.csv'
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
            
df['lesion_result'] = df[['temp', 'rain_block']].apply(lambda x : mills_table(*x), axis=1)


# replace any NaN data with empty string

df = df.replace(np.nan, '')

# print dataframe results




df2 = df.copy()                          # Create duplicate of data

df2.dropna(subset = ['rain_block'], inplace = True)     # Remove rows with NaN


print(df2['rain_block'])


# Export a Pandas Dataframe to CSV
# Relative File Path
df2.to_csv('rain_block')
# Fixed File Path
df2.to_csv('C:\\Users\\proco\\Desktop\\lesion_result.csv')


# old snipets:

#lesion_17_4 = df.loc[((df['temp'] >= 43) & (df['temp'] < 45)) & ((df['rain_block'] > 18))] 
#lesion_17_3 = df.loc[((df['temp'] >= 45) & (df['temp'] < 46)) & ((df['rain_block'] > 15))]
#lesion_17_2 = df.loc[((df['temp'] >= 46) & (df['temp'] < 48)) & ((df['rain_block'] > 13))]
#lesion_17_1= df.loc[((df['temp'] >= 48) & (df['temp'] < 50)) & ((df['rain_block'] > 12))]
#lesion_16 = df.loc[((df['temp'] >= 50) & (df['temp'] < 52)) & ((df['rain_block'] > 11))]
#lesion_15 = df.loc[((df['temp'] >= 52) & (df['temp'] < 54)) & ((df['rain_block'] >  9))]
#lesion_14 = df.loc[((df['temp'] >= 54) & (df['temp'] < 57)) & ((df['rain_block'] > 8))]
#lesion_11_13 = df.loc[((df['temp'] >= 57) & (df['temp'] < 60)) & ((df['rain_block'] > 7))]
#lesion= df.loc[((df['temp'] >= 60) & (df['temp'] < 76)) & ((df['rain_block'] > 6))]

#df['infection_event'] = lesion_17_4['rain_block'].apply(lambda x: 'lesions in 17 days' if x >= 18 else '')
#df['infection_event'] = lesion_17_3['rain_block'].apply(lambda x: 'lesions in 16 days' if x >= 15 else '')
#df['infection_event'] = lesion_17_2['rain_block'].apply(lambda x: 'lesions in 15 days' if x >= 13 else '')
#df['infection_event'] = lesion_17_1['rain_block'].apply(lambda x: 'lesions in 17 days' if x >= 12 else '')
#df['infection_event'] = lesion_16['rain_block'].apply(lambda x: 'lesions in 16 days' if x >= 11 else '')
#df['infection_event'] = lesion_15['rain_block'].apply(lambda x: 'lesions in 15 days' if x >= 9 else '')
#df['infection_event'] = lesion_14['rain_block'].apply(lambda x: 'lesions in 14 days' if x >= 8 else '')
#df['infection_event'] = lesion_11_13['rain_block'].apply(lambda x: 'lesions in 11-13 days' if x >= 7 else '')
#df['infection_event'] = lesion_9_10['rain_block'].apply(lambda x: 'lesions in 9-10 days' if x >= 6 and x < 7 else '')

#df = df[df["infection_event"].str.contains("lesions in 17 days|lesions in 16 days|lesions in 15 days|lesions in 14 days|lesions in 11-13 days|lesions in 9-10 days")]

#print(df['infection_event'])

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