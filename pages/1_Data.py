import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Get the path of the current file (file1.py)
current_file_path = Path(__file__).resolve()
# Get the parent directory (folder1)
parent_dir = current_file_path.parent
# Get the path to the other folder (folder2)
other_folder_path = parent_dir.parent / "lib"
# Add the other folder to sys.path so Python can find the module
sys.path.append(str(other_folder_path))
# Now you can import from file2.py
from utils import data_setup, parse_text_entry, save_numpy_array, generate_class_data, generate_anomaly_data, generate_regression_data

st.title("Data")

sep_labels = False
split = 0.00

if st.button("Clear All Data"):
    sep_labels = False
    split = 0.00
    data = None
    labels = None
    st.session_state["X_train"] = ""
    st.session_state["y_train"] = ""
    st.session_state["X_test"] = ""
    st.session_state["y_test"] = ""
    st.session_state["header check"] = False
    st.session_state["label check"] = False
    st.session_state["seperate labels"] = False
    st.session_state["split data"] = False
    st.session_state["split value:"] = 0.00
    st.session_state["ready to load"] = False
    st.session_state["data loader"] = None
    st.session_state["label loader"] = None


option = st.selectbox('What data would you like to use?',
    ('.csv or .npy file', 'generate waveforms', 'generate scg signals'))


# .CSV or .NPY File Load Options
if option == '.csv or .npy file':
    header_check = st.checkbox("Does your data/label file(s) have headers? Check for yes",key="header check")

if option == '.csv or .npy file':
    label_check = st.checkbox("Does your data file contain labels? Check for yes",key="label check")

if option == '.csv or .npy file' and label_check == False:
    sep_label_check = st.checkbox("Do you have labels in a seperate file? Check for yes",key="seperate labels")
    if sep_label_check == True:
        sep_labels = sep_label_check

if option == '.csv or .npy file':
    split_check = st.checkbox("Select if you will require a train/test split on your data", key = "split data")

    if split_check == True:
        split_value = st.number_input("Enter a float value for you data split:", value=0.0, step=0.01, format="%.2f",key="split value")
        if split_value != 0.00:
            split = split_value

# Generate Wavefor Data Options
elif option == 'generate waveforms':
    wav_cat = st.text_input("Category: classification, detection, or regression", value='classification', key="category")
    wav_amp = st.number_input("Amplitude: float, 0.00 for None", value=0.00, step=0.01, format="%.2f", key="wave amp")
    wav_freq = st.number_input("Frequency: float, 0.00 for None", value=0.00, step=0.01, format="%.2f", key="wave freq")
    wav_noise = st.checkbox("Check to add Noise", key="wave noise box")
    wav_num = st.number_input("Wave Number: integer", value='10', min_value='int', key="wave num")
    wav_label = st.text_input("Labels: amplitude or frequency", value='frequency', key="wave labels")

   
    if st.button("Generate the Wave Data"):
        if wav_amp == 0.0:
            wav_amp = None
        if wav_freq == 0.0:
            wav_freq == None
        
        if wav_cat == 'classification':
            data, labels = generate_class_data(amplitude=wav_amp,frequency=wav_freq,noise=wav_noise,wav_number=wav_num,show=True)
        elif wav_cat == 'detection':
            data, labels = generate_anomaly_data(amplitude=wav_amp,frequency=wav_freq,noise=wav_noise,wave_number=wav_num,show=True)
        else:
            data, labels = generate_regression_data(amplitude=wav_amp,frequency=wav_freq,noise=wav_noise,wave_number=wave_num,label_type=wav_label,show=True)

        labels = labels.reshape(-1, 1)
        data_file = np.concatenate((data,labels),axis=1)

        save_numpy_array(data_file)

elif option == 'generate scg signals':
    st.write("generate scg signals selected")


ready = st.checkbox("Select when ready to choose your file(s)",key = "ready to load")

if ready == True:
    uploaded_file = st.file_uploader("Choose a CSV or NPY data file", type=["csv","npy"],key="data loader")

    if sep_labels == True:
        uploaded_labels = st.file_uploader("Choose a CSV or NPY label file", type=["csv","npy"],key="label loader")
        if uploaded_labels is not None:
            root, extension = os.path.splitext(uploaded_labels.name)
            if extension.lower() == ".npy":
                labels = np.load(uploaded_labels)                
            else:
                if header_check == False:
                    df = pd.read_csv(uploaded_labels,header=None)
                else:
                    df = pd.read_csv(uploaded_labels)
                labels = df.to_numpy
    else:
        labels = None


    if uploaded_file is not None:
        root, extension = os.path.splitext(uploaded_file.name)
        if extension.lower() == ".npy":
            data = np.load(uploaded_file)
            df = pd.DataFrame(data)                
        else:
            if header_check == False:
                df = pd.read_csv(uploaded_file,header=None)
            else:
                df = pd.read_csv(uploaded_file)
            data = df.to_numpy 

        st.write("File uploaded ...")

        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Data Summary")
        st.write(df.describe())    
    
    else:
        st.write("Waiting on file upload")

    if (uploaded_file is not None) and (sep_labels == True):
        X_train, y_train, X_test, y_test = data_setup(label_bool=label_check,
                                                        sep_data_bool=sep_labels,
                                                        split_bool=split_check,
                                                        data_file=data,
                                                        split_value=split,
                                                        label_file=labels)
        st.session_state["X_train"] = X_train
        st.session_state["y_train"] = y_train
        st.session_state["X_test"] = X_test
        st.session_state["y_test"] = y_test
    elif (uploaded_file is not None) and (sep_labels == False):
        X_train, y_train, X_test, y_test = data_setup(label_bool=label_check,
                                                        sep_data_bool=sep_labels,
                                                        split_bool=split_check,
                                                        data_file=data,
                                                        split_value=split,
                                                        label_file=labels)
        st.session_state["X_train"] = X_train
        st.session_state["y_train"] = y_train
        st.session_state["X_test"] = X_test
        st.session_state["y_test"] = y_test
