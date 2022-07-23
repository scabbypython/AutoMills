import pandas as pd
import numpy as np


# this code correctly resamples 5 minute to hour dates, however, as it uses mean, it takes the mean temp and rainfall for that period (I think), I think 
# we want total rainfall for period and the temp may be average or not included there as we are using the blocks max/min
# read in .csv file 'index' column should be date coumn

file = 'Mills_Table_data.csv'
df = pd.read_csv(file, parse_dates=['index'], index_col=['index'],usecols= ['index', 'rain', 'temp'])


# resample 5 minute data to hourly data using mean

df_hour = df.resample('H').mean()




print(df_hour)