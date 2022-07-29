import datetime as dt



#import software libraries
import pandas as pd
import numpy as np


#read file
file = 'infection_comparison.xlsx'

df = pd.read_csv(file, sep = ',', parse_dates=['index'], usecols= ['index', 'rain', 'temp'])

dates = [('index')]
x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]
y = range(len(x)) # many thanks to Kyss Tao for setting me straight here
