# -*- coding: utf-8 -*-

import os
import scipy
import scipy.io
import numpy as np
import pandas as pd
from pathlib import Path
import math
import scipy.signal as signal


p = Path('.')
datapath = p / "data_new/IM_case/"

original_fs = 10000
target_fs = 8000

def downsample_signal(x, original_rate, target_rate):
    """Downsamples a signal from original_rate to target_rate."""

    num_samples = int(len(x) * target_rate / original_rate)
    return signal.resample(x, num_samples)

data_files = [f for f in os.listdir(datapath) if f.endswith('.xlsx')]


df = pd.read_excel(datapath / data_files[0])
df = df.iloc[:109959]
df = df.drop(df.columns[[0,1,2,3]],axis=1).copy()
ds_array = df.to_numpy(dtype=float)
#print("ds_array shape is ",ds_array.shape)
#print(len(ds_array)," is the ds_array length")
f_ds = downsample_signal(ds_array,original_fs,target_fs)
ar_len = len(f_ds)
#print(ar_len," is the ar_len length")

#"""
data = np.empty((0,ar_len+3))
#print("Data shape: ",data.shape)
count = 0
for f in data_files:
    df_temp = pd.read_excel(datapath / f)
    df_temp = df_temp.iloc[:109959]
    df_temp = df_temp.drop(df_temp.columns[[0,1,2,3]],axis=1).copy()
    #num_rows = len(df_temp)
    #print("num rows is ",num_rows)

    temp = df_temp.to_numpy(dtype=float)#.transpose()
    #print("temp shape is ",temp.shape)
    temp = downsample_signal(temp,original_fs,target_fs)
    #print("new temp shape is ",temp.shape)

    
    # Create Labels
    if (('normal' in f) or ('rpm' in f)) == True:        
        temp = np.append(temp,[0.0])
        temp = np.append(temp,[0.0])
    elif (('20' in f) or ('10' in f)) == True:
        temp = np.append(temp,[5.0])
        temp = np.append(temp,[1.0])
    elif (('19' in f)  or ('9' in f)) == True:
        temp = np.append(temp,[4.5])
        temp = np.append(temp,[1.0])
    elif (('18' in f)  or ('8' in f)) == True:
        temp = np.append(temp,[4.0])
        temp = np.append(temp,[1.0])
    elif (('17' in f)  or ('7' in f)) == True:
        temp = np.append(temp,[3.5])
        temp = np.append(temp,[1.0])
    elif (('16' in f)  or ('6' in f)) == True:
        temp = np.append(temp,[3.0])
        temp = np.append(temp,[1.0])
    elif (('15' in f)  or ('5' in f)) == True:
        temp = np.append(temp,[2.5])
        temp = np.append(temp,[1.0])
    elif (('40' in f) or ('14' in f)  or ('4' in f)) == True:
        temp = np.append(temp,[2.0])
        temp = np.append(temp,[1.0])
    elif (('39' in f)) == True:
        temp = np.append(temp,[1.6])
        temp = np.append(temp,[1.0])
    elif (('38' in f)) == True:
        temp = np.append(temp,[1.8])
        temp = np.append(temp,[1.0])
    elif (('37' in f)) == True:
        temp = np.append(temp,[1.4])
        temp = np.append(temp,[1.0])
    elif (('36' in f)) == True:
        temp = np.append(temp,[1.2])
        temp = np.append(temp,[1.0])
    elif (('35' in f)) == True:
        temp = np.append(temp,[1.0])
        temp = np.append(temp,[1.0])
    elif (('34' in f)) == True:
        temp = np.append(temp,[0.8])
        temp = np.append(temp,[1.0])
    elif (('33' in f)) == True:
        temp = np.append(temp,[0.6])
        temp = np.append(temp,[1.0])
    elif (('32' in f)) == True:
        temp = np.append(temp,[0.4])
        temp = np.append(temp,[1.0])
    elif (('31' in f)) == True:
        temp = np.append(temp,[0.2])
        temp = np.append(temp,[1.0])
    elif (('13' in f)  or ('3' in f)) == True:
        temp = np.append(temp,[1.5])
        temp = np.append(temp,[1.0])
    elif (('12' in f)  or ('2' in f)) == True:
        temp = np.append(temp,[1.0])
        temp = np.append(temp,[1.0])
    elif (('11' in f)  or ('1' in f)) == True:
        temp = np.append(temp,[0.5])
        temp = np.append(temp,[1.0])
    else:
        temp = np.append(temp,[0.0])

    if (('normal' in f) ) == True:        
        temp = np.append(temp,['Normal'])
    elif (('20' in f) or ('19' in f) or ('18' in f) or ('17' in f) or ('16' in f) or ('15' in f)
          or ('14' in f) or ('13' in f) or ('12' in f) or ('111' in f)) == True:
        temp = np.append(temp,['A'])
    else:
        temp = np.append(temp,['A&B'])

    #print("appended shape is ",temp.shape)
    normal = temp.reshape(1,ar_len+3)
    #print("normal shape is ",normal.shape)

    data = np.append(data,normal,axis=0)
    #print("data shape is ",data.shape)
    #data = np.append(data,temp_normal,axis=0)
    #data = np.append(data,temp_anomaly,axis=0)

    #np.save("test_shape.npy",normal)
    #count += 1
    #if count == 2:
        #exit(0)

   
print("data shape is ", data.shape)

#data = convert_to_float_array(data)
np.save("smartplug_feature_8k.npy",data)
print("COMPLETE")
#"""