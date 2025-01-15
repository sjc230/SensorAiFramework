# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 13:42:44 2021

@author: steph

converts .mat files to .csv files and adds labels
"""

import os
import seaborn as sns; sns.set()
import scipy
import scipy.io
import numpy as np
import pandas as pd
from pathlib import Path

# 800,000 samples per .mat file
# 40 seconds worth of samples per .mat file
# 20,000 samples per second

N = 800000
ss = 20000
anom_start = int(ss*15)
anom_end = int(ss*25)
con_start = int(ss*14.75) #0.25sec of normal data before anomaly
con_end = int(ss*16.5) #ends with 1.5 sec of anomaly data


p = Path('.')
datapath = p / "Data/"
trainpath = p / "TrainData/"
testpath = p / "TestData/"

# Column Names
col_names = ['Time','V1','V2','V3','C1','C2','C3']
label_name = ['Label']

# create labels for dataset
normal_array = np.zeros(N)

dia_array = normal_array.copy()
for i in range(anom_start,anom_end):
    dia_array[i] = int(1)
df_diaLabel = pd.DataFrame(dia_array, columns=['Label'])
print('dia count: ',df_diaLabel.value_counts())

cdia_array = normal_array.copy()
for j in range(anom_start,anom_end):
    cdia_array[j] = int(2)    
df_cdiaLabel = pd.DataFrame(cdia_array, columns=['Label'])
print('cdia count: ',df_cdiaLabel.value_counts())

replay_array = normal_array.copy()
for k in range(anom_start,anom_end):
    replay_array[k] = int(3)    
df_replayLabel = pd.DataFrame(replay_array, columns=['Label'])
print('replay count: ',df_replayLabel.value_counts())

open_array = normal_array.copy()
for l in range(anom_start,anom_end):
    open_array[l] = int(4)    
df_openLabel = pd.DataFrame(open_array, columns=['Label'])
print('o fault count: ',df_openLabel.value_counts())

short_array = normal_array.copy()
for m in range(anom_start,anom_end):
    short_array[m] = int(5)    
df_shortLabel = pd.DataFrame(short_array, columns=['Label'])
print('s fault count: ',df_shortLabel.value_counts())

data_files = [f for f in os.listdir(datapath) if f.endswith('.mat')]

df_train = pd.DataFrame(columns = col_names)
df_test = pd.DataFrame(columns = col_names)
df_condensed = pd.DataFrame(columns = col_names)
df_trainTruth = pd.DataFrame(columns = label_name)
df_testTruth = pd.DataFrame(columns = label_name)

segment = np.empty([7, con_end-con_start])

for f in data_files:
        temp_file = scipy.io.loadmat(datapath / f, mdict=None, appendmat=True)
        print("TEMP FILE: ",temp_file)
        df_temp = pd.DataFrame(temp_file["gridvoltage"].transpose(), columns = col_names)
        if (('01' in f) or ('02' in f) or ('03' in f) or ('04' in f) or ('05' in f) or ('06' in f) or ('14' in f) or ('15' in f) or ('16' in f) or ('17' in f) or ('18' in f) or ('19' in f)) == True:
            df_train = df_train.append(df_temp,ignore_index=True)
            df_trainTruth = df_trainTruth.append(df_diaLabel,ignore_index=True)
            print("file added to Training set: ",f)
            if (('01' in f)  or ('04' in f) or ('14' in f)) == True:
                temp_seg = df_temp.to_numpy().transpose()
                segment[:, :] = temp_seg[:,con_start:con_end]
                df_segment = pd.DataFrame(segment.transpose(),columns = col_names)
                df_condensed = df_condensed.append(df_segment,ignore_index=True)
                print("segment added to Condensed set: ",f)
        elif (('07' in f) or ('08' in f) or ('20' in f) or ('24' in f)) == True:
            df_test = df_test.append(df_temp,ignore_index=True)
            df_testTruth = df_testTruth.append(df_diaLabel,ignore_index=True)
            print("file added to Test set: ",f)            
        elif (('09' in f) or ('10' in f) or ('11' in f) or ('12' in f) or ('13' in f) or ('21' in f) or ('25' in f) or ('26' in f) or ('33' in f)) == True:
            df_train = df_train.append(df_temp,ignore_index=True)
            df_trainTruth = df_trainTruth.append(df_cdiaLabel,ignore_index=True)
            print("file added to Training set: ",f)
            if (('09' in f) or ('25' in f)) == True:
                temp_seg = df_temp.to_numpy().transpose()
                segment[:, :] = temp_seg[:,con_start:con_end]
                df_segment = pd.DataFrame(segment.transpose(),columns = col_names)
                df_condensed = df_condensed.append(df_segment,ignore_index=True)
                print("segment added to Condensed set: ",f)
        elif (('22' in f) or ('23' in f) or ('36' in f)) == True:
            df_test = df_test.append(df_temp,ignore_index=True)
            df_testTruth = df_testTruth.append(df_cdiaLabel,ignore_index=True)
            print("file added to Test set: ",f)
        elif ('27' in f) == True:
            df_train = df_train.append(df_temp,ignore_index=True)
            df_trainTruth = df_trainTruth.append(df_replayLabel,ignore_index=True)
            print("file added to Training set: ",f)
            if ('27' in f)  == True:
                temp_seg = df_temp.to_numpy().transpose()
                segment[:, :] = temp_seg[:,con_start:con_end]
                df_segment = pd.DataFrame(segment.transpose(),columns = col_names)
                df_condensed = df_condensed.append(df_segment,ignore_index=True)
                print("segment added to Condensed set: ",f)
        elif ('45' in f) == True:
            df_test = df_test.append(df_temp,ignore_index=True)
            df_testTruth = df_testTruth.append(df_replayLabel,ignore_index=True)
            print("file added to Test set: ",f)
        elif (('39' in f) or ('46' in f) or ('48' in f) or ('49' in f) or ('50' in f) or ('51' in f) or ('52' in f) or ('53' in f) or ('54' in f) or ('57' in f) or ('58' in f)) == True:
            df_train = df_train.append(df_temp,ignore_index=True)
            df_trainTruth = df_trainTruth.append(df_shortLabel,ignore_index=True)
            print("file added to Training set: ",f)
            if (('39' in f) or ('46' in f) or ('51' in f)) == True:
                temp_seg = df_temp.to_numpy().transpose()
                segment[:, :] = temp_seg[:,con_start:con_end]
                df_segment = pd.DataFrame(segment.transpose(),columns = col_names)
                df_condensed = df_condensed.append(df_segment,ignore_index=True)
                print("segment added to Condensed set: ",f)
        elif (('47' in f) or ('55' in f) or ('56' in f) or ('59' in f)) == True:
            df_test = df_test.append(df_temp,ignore_index=True)
            df_testTruth = df_testTruth.append(df_shortLabel,ignore_index=True)
            print("file added to Test set: ",f)
        elif (('31' in f) or ('60' in f) or ('61' in f)) == True:
            df_train = df_train.append(df_temp,ignore_index=True)
            df_trainTruth = df_trainTruth.append(df_openLabel,ignore_index=True)
            print("file added to Training set: ",f)
            if (('31' in f) or ('60' in f)) == True:
                temp_seg = df_temp.to_numpy().transpose()
                segment[:, :] = temp_seg[:,con_start:con_end]
                df_segment = pd.DataFrame(segment.transpose(),columns = col_names)
                df_condensed = df_condensed.append(df_segment,ignore_index=True)
                print("segment added to Condensed set: ",f)
        elif ('62' in f) == True:
            df_test = df_test.append(df_temp,ignore_index=True)
            df_testTruth = df_testTruth.append(df_openLabel,ignore_index=True)
            print("file added to Test set: ",f)
        else:
            print("file not part of Training or Test set: ",f)
    
df_train.to_csv(trainpath / 'train_data.csv', index=False)
df_test.to_csv(testpath / 'test_data.csv', index=False)

df_trainTruth.to_csv(trainpath / 'train_labels.csv', index=False)
df_testTruth.to_csv(testpath / 'test_labels.csv', index=False)

df_condensed.to_csv(datapath / 'condensed_data.csv', index=False)
