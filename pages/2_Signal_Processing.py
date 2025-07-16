import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import time

# Get the path of the current file (file1.py)
current_file_path = Path(__file__).resolve()
# Get the parent directory (folder1)
parent_dir = current_file_path.parent
# Get the path to the other folder (folder2)
other_folder_path = parent_dir.parent / "lib"
# Add the other folder to sys.path so Python can find the module
sys.path.append(str(other_folder_path))
# Now you can import from file2.py
from utils import parse_text_entry, display_log_updates
from dsp import *


def active_save_verification(signal):
    if make_active_check == True:
        st.session_state["active_dataset"] = signal
        st.write(st.session_state["active_dataset"])
    if save_output_check == True:
        save_numpy_array(signal)
        st.write("Noisy Data saved to .npy file")

st.title("Digital Signal Processing")

dsp_tuple = ('noise generation', 'filtering', 'time & frequency domain features', 'signal decomposition',
               'wavelet analysis', 'transforms')

noise_tuple = ('white', 'impulse', 'burst', 'brown', 
               'pine', 'flicker', 'powerline', 'resonance')

white_noise_tuple = ('gaussian', 'laplacian', 'band-limited')

make_active_check = st.checkbox("Would you like to make the results your active data file?",key="make active check")
save_output_check = st.checkbox("Would you like to save the output as a .npy file?",key="save output check")

dsp_box = st.selectbox('**Select the type of processing to perform.**', dsp_tuple)

if dsp_box == 'noise generation':
    noise_box = st.selectbox('**Select the type of noise**', noise_tuple)

if noise_box == 'white' and dsp_box == 'noise generation':
    white_type_box = st.selectbox('**Select the type of white noise**', white_noise_tuple)

if dsp_box == 'noise generation':
    noise_amp = st.number_input(label='noise amplitude',step=0.01,format="%.02f",value=0.3)

if  noise_box == 'white' and dsp_box == 'noise generation' and white_type_box == 'band-limited':
    blw_lc = st.number_input(label='noise low cutoff frequency',step=0.01,format="%.02f",value=0.01)
    blw_hc = st.number_input(label='noise high cutoff frequency',step=0.01,format="%.02f",value=10.0)
    blw_sr = st.number_input(label='band-limited sampling rate',min_value=0,step=1,value=100)
    blw_or = st.number_input(label='band-limited order',min_value=0,step=1,value=3)

if not str(st.session_state["active_dataset"]) == "" and noise_box == 'white' and dsp_box == 'noise generation':
    if st.button("Add White Noise to Signal"):
        noisy_signal = st.session_state["active_dataset"].copy()
        wr_count = 0
        for row in noisy_signal:
            if wr_count == 0:
                show = True
            else:
                show = False

            if white_type_box == 'gaussian':
                noisy_row = add_white_noise(signal=row, noise_amplitude=noise_amp, model=0, show=show, stream=show)
                noisy_signal[wr_count] = noisy_row
            elif white_type_box == 'laplacian':
                noisy_row = add_white_noise(signal=row, noise_amplitude=noise_amp, model=1, show=show, stream=show)
                noisy_signal[wr_count] = noisy_row
            elif white_type_box == 'band-limited':
                noisy_row = add_band_limited_white_noise(signal=row, noise_amplitude=noise_amp, lowcut=blw_lc, highcut=blw_hc, 
                                            sampling_rate=blw_sr, order=blw_or, show=show, stream=show)
                noisy_signal[wr_count] = noisy_row

            wr_count += 1
        
        active_save_verification(noisy_signal)

if noise_box == 'impulse' and dsp_box == 'noise generation':
    add_imp_rate = st.checkbox("Add an impulse rate", value=False, key="add_impulse_rate")
    if add_imp_rate == True:
        imp_rt = st.number_input(label='impulse rate',step=0.01,format="%.02f",value=0.5)
    else:
        imp_rt = None

    add_imp_num = st.checkbox("Add more than one impulse", value=False, key="add_impulse_number")
    if add_imp_num == True:
        imp_num = st.number_input(label='number of impulses',min_value=0,step=1,value=2)
    else:
        imp_num = None

if not str(st.session_state["active_dataset"]) == "" and noise_box == 'impulse' and dsp_box == 'noise generation':
    if st.button("Add Impulse Noise to Signal"):
        noisy_signal = st.session_state["active_dataset"].copy()
        ir_count = 0
        for row in noisy_signal:           
            if ir_count == 0:
                show = True
                #print(show)
            else:
                show = False
            noisy_row = add_impulsive_noise(signal=row, noise_amplitude=noise_amp, rate=imp_rt, 
                                            number=imp_num, show=show, stream=show)
            print(noisy_row)
            noisy_signal[ir_count] = noisy_row
            ir_count += 1

        print("I'm Here")    
        active_save_verification(noisy_signal)