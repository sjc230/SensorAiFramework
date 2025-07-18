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

##########################################################
# NOISE GENERATION
##########################################################

noise_tuple = ('white', 'impulse', 'burst', 'colored', 
               'echo', 'flicker', 'powerline')

white_noise_tuple = ('gaussian', 'laplacian', 'band-limited')

color_noise_tuple = ('blue', 'brown', 'pink')

make_active_check = st.checkbox("Would you like to make the results your active data file?",key="make active check")
save_output_check = st.checkbox("Would you like to save the output as a .npy file?",key="save output check")

dsp_box = st.selectbox('**Select the type of processing to perform.**', dsp_tuple)

if dsp_box == 'noise generation':    
    noise_box = st.selectbox('**Select the type of noise**', noise_tuple)

if dsp_box == 'noise generation':
    if noise_box == 'white':
        white_type_box = st.selectbox('**Select the type of white noise**', white_noise_tuple)

if dsp_box == 'noise generation':
    if noise_box == 'colored':
        color_box = st.selectbox('**Select the color of noise**', color_noise_tuple,key='color_noise_box')

if dsp_box == 'noise generation':
    if noise_box != 'echo':
        noise_amp = st.number_input(label='noise amplitude',step=0.01,format="%.02f",value=0.3,key='noise_amplitude_box')

if  dsp_box == 'noise generation':
    if noise_box == 'white' and white_type_box == 'band-limited':
        blw_lc = st.number_input(label='noise low cutoff frequency',step=0.01,format="%.02f",value=0.01)
        blw_hc = st.number_input(label='noise high cutoff frequency',step=0.01,format="%.02f",value=10.0)
        blw_sr = st.number_input(label='band-limited sampling rate',min_value=0,step=1,value=100)
        blw_or = st.number_input(label='band-limited order',min_value=0,step=1,value=3)

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'white':
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

if dsp_box == 'noise generation':
    if noise_box == 'impulse':
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

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'impulse':
        if st.button("Add Impulse Noise to Signal"):
            noisy_signal = st.session_state["active_dataset"].copy()
            ir_count = 0
            for row in noisy_signal:           
                if ir_count == 0:
                    show = True
                else:
                    show = False
                noisy_row = add_impulsive_noise(signal=row, noise_amplitude=noise_amp, rate=imp_rt, 
                                                number=imp_num, show=show, stream=show)
                noisy_signal[ir_count] = noisy_row
                ir_count += 1
    
            active_save_verification(noisy_signal)


if dsp_box == 'noise generation':
    if noise_box == 'burst':
        brst_num_max = st.number_input(label='max number of burst noise events to add',min_value=1,step=1,value=1, key="burst_number_maximum")
        brst_dur = st.text_input(label='burst duration: list minimum and maximum, integers',value='1,2', key="burst_duration")    

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'burst':
        if st.button("Add Impulse Noise to Signal"):
            brst_dur_list = parse_text_entry(brst_dur,'int') 
            noisy_signal = st.session_state["active_dataset"].copy()
            br_count = 0
            for row in noisy_signal:
                if br_count == 0:
                    show = True
                else:
                    show = False
                noisy_row = add_burst_noise(signal=row, noise_amplitude=noise_amp, 
                                                burst_num_max=brst_num_max, burst_durations=brst_dur_list, 
                                                show=show, stream=show)
                noisy_signal[br_count] = noisy_row
                br_count += 1
    
            active_save_verification(noisy_signal)
    
if  dsp_box == 'noise generation':
    if noise_box == 'colored':
        clr_sam_rt = st.number_input(label='sampling rate',min_value=1,step=1,value=100,key='color_noise_sampling_rate')
        clr_dur = st.number_input(label='duration',min_value=1,step=1,value=10,key='color_noise_duration')

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'colored':
        if st.button("Add Colored Noise to Signal"):
            noisy_signal = st.session_state["active_dataset"].copy()
            cr_count = 0
            for row in noisy_signal:
                if cr_count == 0:
                    show = True
                else:
                    show = False

                noisy_row = add_colored_noise(signal=row, noise_amplitude=noise_amp, model=str(color_box), sampling_rate=int(clr_dur), 
                                            duration=int(clr_dur), show=show, stream=show)
                noisy_signal[cr_count] = noisy_row
                cr_count += 1
            
            active_save_verification(noisy_signal)


if dsp_box == 'noise generation':
    if noise_box == 'echo':
        echo_num = st.number_input(label='number of echos: single integer',min_value=1,step=1,value=2, key="echo_number")
        echo_att = st.text_input(label='echo attenuation factors: must have an entry for each echo number',value='0.5,0.4', key="echo_attenuation_factor")
        echo_del = st.text_input(label='echo delay factor: delay for each echoe, must have same number of entries as echo numers',value='5,5', key="echo_delay_factor")  

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'echo':
        if st.button("Add Echo Noise to Signal"):
            echo_att_list = parse_text_entry(echo_att,'float')
            echo_del_list = parse_text_entry(echo_del,'int') 
            noisy_signal = st.session_state["active_dataset"].copy()
            er_count = 0
            for row in noisy_signal:
                if er_count == 0:
                    show = True
                else:
                    show = False
                noisy_row = add_echo_noise(signal=row, n_echo=echo_num, 
                                           attenuation_factor=echo_att_list, delay_factor=echo_del_list,
                                           show=show, stream=show)
                noisy_signal[er_count] = noisy_row
                er_count += 1
    
            active_save_verification(noisy_signal)

if dsp_box == 'noise generation':
    if noise_box == 'flicker':
        flk_sr = st.number_input(label='flicker sampling rate: float',min_value=1,step=1,value=10, key="flicker_sampling_rate")
        flk_dur = st.number_input(label='flicker duration: float',min_value=1,step=1,value=2, key="flicker_duration")

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'flicker':
        if st.button("Add Flicker Noise to Signal"):
            noisy_signal = st.session_state["active_dataset"].copy()
            fr_count = 0
            for row in noisy_signal:
                if fr_count == 0:
                    show = True
                else:
                    show = False
                noisy_row = add_flicker_noise(signal=row, noise_amplitude=noise_amp, 
                                              sampling_rate=flk_sr, duration=flk_dur,
                                              show=show, stream=show)
                noisy_signal[fr_count] = noisy_row
                fr_count += 1
    
            active_save_verification(noisy_signal)


if dsp_box == 'noise generation':
    if noise_box == 'powerline':
        pow_sr = st.number_input(label='sampling rate',min_value=1,step=1,value=2, key="powerline_sampling_rate")
        pow_dur = st.number_input(label='powerline duration',min_value=1,step=1,value=2, key="powerline_duration")
        pow_frq = st.number_input(label='powerline frequency',min_value=1,step=1,value=50, key="powerline_frequency")

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'powerline':
        if st.button("Add Powerline Noise to Signal"):
            noisy_signal = st.session_state["active_dataset"].copy()
            pr_count = 0
            for row in noisy_signal:
                if pr_count == 0:
                    show = True
                else:
                    show = False
                noisy_row = add_powerline_noise(signal=row, sampling_rate=pow_sr, duration=pow_dur,
                                                powerline_frequency=pow_frq, powerline_amplitude=noise_amp,
                                                show=show, stream=show)
                noisy_signal[pr_count] = noisy_row
                pr_count += 1
    
            active_save_verification(noisy_signal)
