# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
 
 
file = r'C:\Users\ResononScanningSyst\Documents\GitHub\AutoMills\5min_hour_comparison_test_2.csv'

df = pd.read_csv(file, sep = ',', parse_dates=['index'] , usecols= ['index', 'a11', 'a16','north_e','north_m','north_x','north','south_g','south_y','south'])





print(df)
  
# plot data in stack manner of bar type
df.plot(x='index', kind='bar', stacked=True,
        title='Stacked Bar Graph by dataframe')

y = np.array([1, 3, 5, 7,9,11,13,15,17])

ticks = ['a11','a16','north_e','north_m','north_x','north','south_g','south_y','south']
plt.yticks(y, ticks)
# Show graphic
plt.show()