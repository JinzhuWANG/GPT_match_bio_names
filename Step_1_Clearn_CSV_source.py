import pandas as pd
import numpy as np

from tools import clean_csv




# Read data
df_fauna = clean_csv('data/EPBC Act List of Threatened Fauna.csv')
df_flora = clean_csv('data/EPBC Act List of Threatened Flora.csv')
df = pd.concat([df_fauna, df_flora], axis=0).reset_index(drop=True)
    


df

