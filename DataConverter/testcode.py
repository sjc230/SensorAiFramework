# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 13:42:44 2021

@author: steph

converts .mat files to .csv files and adds labels
"""

import os
#import seaborn as sns; sns.set_theme()
import scipy
import scipy.io
import numpy as np
import pandas as pd
from pathlib import Path
#import matplotlib.pyplot as plt
import math


# Define a function named 'every_nth' that returns every nth element from a list.
# It takes two parameters: 'nums' (the list) and 'nth' (the interval for selecting elements).
def every_nth(nums, nth):
    # Use list slicing to return elements starting from the (nth-1) index, with a step of 'nth'.
    return nums[nth - 1::nth]

# Define a function named 'every_10th' that returns every 10th element from a numpy array.
# It takes one parameter: 'nums' (the array).
def every_10th(nums):
    # Use list slicing to return elements starting from the (nth-1) index, with a step of 'nth'.
    return nums[::10]

def convert_to_float_array(array_of_lists):
    return np.array(array_of_lists, dtype=float)

p = Path('.')
datapath = p / "data/PCC/"


# Column Names
col_names = ['C1','C2','C3']
label_name = ['Label']

drop_columns = [0,1]

# Create Dataframe to hold final dataset
df_data = pd.DataFrame(columns = col_names)
df_labels = pd.DataFrame(columns = label_name)

# create labels for dataset
#normal_array = np.zeros(N)

#df = pd.read_csv(datapath / 'AdaSST_Case_1.csv')
#print(df.shape)
#df_c1 = df.drop(df.columns[[1,2]],axis=1).copy()

#df_c1.plot(kind='line') # Line plot (default)
#plt.show()

data_files = [f for f in os.listdir(datapath) if f.endswith('.csv')]

# Normal = 0
# Bearing Fault = 1
# Inter-turn Fault = 2
# FDI Attack = 3

data = np.empty((0,2001),float)
#print("Data shape: ",data.shape)

for f in data_files:
    df_temp = pd.read_csv(datapath / f, header=None, dtype=float)
    df_temp = df_temp.drop(df_temp.columns[[1,2]],axis=1).copy()
    num_rows = len(df_temp)
    #print(num_rows)
    if num_rows == 40000:
        df_temp_normal = df_temp.iloc[:20000]    
        df_temp_anomaly = df_temp.iloc[20000:]
    else:
        df_temp_normal = df_temp.iloc[:2000]    
        df_temp_anomaly = df_temp.iloc[2000:]
    temp_normal = df_temp_normal.to_numpy(dtype=float)#.transpose()
    #print(temp_normal.shape," is the shape")
    temp_anomaly = df_temp_anomaly.to_numpy(dtype=float)#.transpose()
    #print(temp_anomaly)
    #for element in temp_anomaly:
    #    print(type(element[0])," element type")
    #    print(len(element)," len")
    if num_rows == 40000:
        temp_normal = every_10th(temp_normal)
    temp_normal = np.append(temp_normal,[0])
    """
    temp_normal_list = temp_normal.tolist()
    if num_rows == 40000:
        temp_normal_list = every_nth(temp_normal_list,10)
        #print(temp_normal.shape," is the shape")
    temp_normal_list.append(0)
    #"""
    #print("Norm len: ",len(temp_normal_list)," ",f)
    if num_rows == 40000:
        temp_anomaly = every_10th(temp_anomaly)
    """
    temp_anomaly_list = temp_anomaly.tolist()
    if num_rows == 40000:
        temp_anomaly_list = every_nth(temp_anomaly_list,10)
    #"""
    # 2 - Inter-turn Fault file check
    if (('120' in f) or ('119' in f) or ('118' in f) or ('117' in f) or ('116' in f) or ('115' in f) or 
        ('114' in f) or ('113' in f) or ('112' in f) or ('111' in f) or ('110' in f) or ('109' in f) or 
        ('108' in f) or ('107' in f) or ('106' in f) or ('105' in f) or ('104' in f) or ('103' in f) or 
        ('102' in f) or ('101' in f) or ('100' in f) or ('99' in f) or ('98' in f) or ('97' in f) or 
        ('96' in f) or ('95' in f) or ('94' in f) or ('93' in f) or ('92' in f) or ('91' in f) or 
        ('90' in f) or ('89' in f) or ('88' in f) or ('87' in f) or ('86' in f) or ('85' in f) or 
        ('84' in f) or ('83' in f) or ('82' in f) or ('81' in f)) == True:
        
        #temp_anomaly_list.append(2)
        temp_anomaly = np.append(temp_anomaly,[2])
        #print("Anom len: ",len(temp_anomaly_list)," ",f)
        #print("Inter-turn Fault")        
    # 1 - All others are Bearing Fault
    else:
        #temp_anomaly_list.append(1)
        temp_anomaly = np.append(temp_anomaly,[1])
        #print("Anom len: ",len(temp_anomaly_list)," ",f)
        #print("Bearing Fault")

    #print(temp_normal_list)
    #normal = np.asarray(temp_normal_list, dtype = object)
    normal = temp_normal.reshape(1,2001)
    #print("normal shape: ",normal.shape)
    #anomaly = np.array(temp_anomaly_list, dtype = object)
    anomaly = temp_anomaly.reshape(1,2001)
    #print("anomaly shape: ",anomaly.shape)
    data = np.append(data,normal,axis=0)
    data = np.append(data,anomaly,axis=0)

    #data = np.append(data,temp_normal,axis=0)
    #data = np.append(data,temp_anomaly,axis=0)

    #print(data.shape)

#data = convert_to_float_array(data)
np.save("smartplug_pcc_c3.npy",data)
print("COMPLETE")