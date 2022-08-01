import pandas as pd
import glob
import os

#csv1 = pd.read_csv(r"C:\Users\ResononScanningSyst\Documents\GitHub\AutoMills\Working_model\AutoMills\leaf_wetness_&_temp_2022_2022_08_01_11_35_07_EDT_1.csv")
#csv1.head()

#csv2 = pd.read_csv(r"C:\Users\ResononScanningSyst\Documents\GitHub\AutoMills\Working_model\AutoMills\leaf_wetness_&_temp_2022_2022_08_01_11_35_07_EDT_2.csv")
#csv2.head()

#merged_data = csv1.merge(csv2,on=["Security Code"])
#merged_data = csv1.merge(csv2)
#merged_data.head()

files = os.path.join("C:\\Users\\ResononScanningSyst\\Desktop\\AutoMills\\merged", "leaf_wetness_&_temp_2022_2022_08_01_11_35_07_EDT_*.csv")
                     
files = glob.glob(files)   

df = pd.concat(map(pd.read_csv, files), ignore_index=False)
print(df)   

df.to_csv('leaf_wetness_&_temp_2022_2022_08_01_11_35_07_EDT_merged.csv')