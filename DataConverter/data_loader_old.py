# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 13:42:44 2021

@author: steph
"""

import os
import seaborn as sns; sns.set()
import scipy
import scipy.io
import pandas as pd
from pathlib import Path



p = Path('.')
datapath = p / "Data/"

# Column Names
col_names = ['Time','V1','V2','V3','C1','C2','C3']

data_files = [f for f in os.listdir(datapath) if f.endswith('.mat')]

df_data = pd.DataFrame(columns = col_names)

for f in data_files:
    temp_file = scipy.io.loadmat(datapath / f, mdict=None, appendmat=True)
    df_temp = pd.DataFrame(temp_file["gridvoltage"].transpose(), columns = col_names)
    #df_temp.set_index('Time')
    df_data = df_data.append(df_temp,ignore_index=True)
    print("loaded file: ",f)
    
df_data.to_csv(datapath / 'data.csv', index=False)
print("csv file created: data.csv")