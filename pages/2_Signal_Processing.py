import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from scipy.stats import kurtosis, skew
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

st.sidebar.title("Digital Signal Processing")

dsp_tuple = ('noise generation', 'filtering', 'time & frequency domain features', 'signal decomposition',
               'wavelet analysis', 'transforms')

##########################################################
# NOISE GENERATION
##########################################################

noise_tuple = ('white', 'impulse', 'burst', 'colored', 
               'echo', 'flicker', 'powerline')

white_noise_tuple = ('gaussian', 'laplacian', 'band-limited')

color_noise_tuple = ('blue', 'brown', 'pink')

make_active_check = st.sidebar.checkbox("Would you like to make the results your active data file?",key="make active check")
save_output_check = st.sidebar.checkbox("Would you like to save the output as a .npy file?",key="save output check")

dsp_box = st.sidebar.selectbox('**Select the type of processing to perform.**', dsp_tuple)

if dsp_box == 'noise generation':    
    noise_box = st.sidebar.selectbox('**Select the type of noise**', noise_tuple)

if dsp_box == 'noise generation':
    if noise_box == 'white':
        white_type_box = st.sidebar.selectbox('**Select the type of white noise**', white_noise_tuple)

if dsp_box == 'noise generation':
    if noise_box == 'colored':
        color_box = st.sidebar.selectbox('**Select the color of noise**', color_noise_tuple,key='color_noise_box')

if dsp_box == 'noise generation':
    if noise_box != 'echo':
        noise_amp = st.sidebar.number_input(label='noise amplitude',step=0.01,format="%.02f",value=0.3,key='noise_amplitude_box')

if  dsp_box == 'noise generation':
    if noise_box == 'white' and white_type_box == 'band-limited':
        blw_lc = st.sidebar.number_input(label='noise low cutoff frequency',step=0.01,format="%.02f",value=0.01)
        blw_hc = st.sidebar.number_input(label='noise high cutoff frequency',step=0.01,format="%.02f",value=10.0)
        blw_sr = st.sidebar.number_input(label='band-limited sampling rate',min_value=0,step=1,value=100)
        blw_or = st.sidebar.number_input(label='band-limited order',min_value=0,step=1,value=3)

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'white':
        if st.sidebar.button("Add White Noise to Signal"):
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
        add_imp_rate = st.sidebar.checkbox("Add an impulse rate", value=False, key="add_impulse_rate")
        if add_imp_rate == True:
            imp_rt = st.sidebar.number_input(label='impulse rate',step=0.01,format="%.02f",value=0.5)
        else:
            imp_rt = None

        add_imp_num = st.sidebar.checkbox("Add more than one impulse", value=False, key="add_impulse_number")
        if add_imp_num == True:
            imp_num = st.sidebar.number_input(label='number of impulses',min_value=0,step=1,value=2)
        else:
            imp_num = None

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'impulse':
        if st.sidebar.button("Add Impulse Noise to Signal"):
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
        brst_num_max = st.sidebar.number_input(label='max number of burst noise events to add',min_value=1,step=1,value=1, key="burst_number_maximum")
        brst_dur = st.sidebar.text_input(label='burst duration: list minimum and maximum, integers',value='1,2', key="burst_duration")    

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'burst':
        if st.sidebar.button("Add Impulse Noise to Signal"):
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
        clr_sam_rt = st.sidebar.number_input(label='sampling rate',min_value=1,step=1,value=100,key='color_noise_sampling_rate')
        clr_dur = st.sidebar.number_input(label='duration',min_value=1,step=1,value=10,key='color_noise_duration')

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'colored':
        if st.sidebar.button("Add Colored Noise to Signal"):
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
        echo_num = st.sidebar.number_input(label='number of echos: single integer',min_value=1,step=1,value=2, key="echo_number")
        echo_att = st.sidebar.text_input(label='echo attenuation factors: must have an entry for each echo number',value='0.5,0.4', key="echo_attenuation_factor")
        echo_del = st.sidebar.text_input(label='echo delay factor: delay for each echoe, must have same number of entries as echo numers',value='5,5', key="echo_delay_factor")  

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'echo':
        if st.sidebar.button("Add Echo Noise to Signal"):
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
        flk_sr = st.sidebar.number_input(label='flicker sampling rate: float',min_value=1,step=1,value=10, key="flicker_sampling_rate")
        flk_dur = st.sidebar.number_input(label='flicker duration: float',min_value=1,step=1,value=2, key="flicker_duration")

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'flicker':
        if st.sidebar.button("Add Flicker Noise to Signal"):
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
        pow_sr = st.sidebar.number_input(label='sampling rate',min_value=1,step=1,value=2, key="powerline_sampling_rate")
        pow_dur = st.sidebar.number_input(label='powerline duration',min_value=1,step=1,value=2, key="powerline_duration")
        pow_frq = st.sidebar.number_input(label='powerline frequency',min_value=1,step=1,value=50, key="powerline_frequency")

if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'noise generation':
    if noise_box == 'powerline':
        if st.sidebar.button("Add Powerline Noise to Signal"):
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


##########################################################
# FILTERING
##########################################################

filter_tuple = ('butterworth', 'adaptive', 'denoising', 'kalman', 'matched', 'notch', 'sav-gol', 'wiener')

butter_tuple = ('high-pass','low-pass','band-pass','band-stop')

denoise_tuple = ('fft','wavelet')

if dsp_box == 'filtering':
    filter_box = st.sidebar.selectbox('**Select the type of filtering.**', filter_tuple)
            
if dsp_box == 'filtering':
    if filter_box == 'butterworth':
        btt_type = st.sidebar.selectbox('**Select the type of filtering.**', butter_tuple)
        if btt_type == 'high-pass' or btt_type == 'low-pass':
            btt_co = st.sidebar.number_input(label='cutoff frequency',min_value=1,step=1,value=10, key="butterworth_cutoff")
        elif btt_type == 'band-pass' or btt_type == 'band-stop':
            btt_lc = st.sidebar.number_input(label='low cutoff frequency',min_value=1,step=1,value=10, key="butterworth_low_cutoff")
            btt_hc = st.sidebar.number_input(label='high cutoff frequency',min_value=1,step=1,value=10, key="butterworth_high_cutoff")

        btt_sf = st.sidebar.number_input(label='sampling frequency',min_value=1,step=1,value=100, key="butterworth_sampling_frequency")
        btt_or = st.sidebar.number_input(label='order',min_value=1,step=1,value=5, key="butterworth_order")
        
if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'filtering':
    if filter_box == 'butterworth':
        if st.sidebar.button("Filter Signal with Butterworth"):
            filtered_signal = st.session_state["active_dataset"].copy()
            pr_count = 0
            for row in filtered_signal:
                if pr_count == 0:
                    show = True
                else:
                    show = False
                if btt_type == 'high-pass':
                    filtered_row = butter_highpass_filter(signal=row, cutoff=btt_co, fs=btt_sf, 
                                                       order=btt_or, show=show, stream=show)
                elif btt_type == 'low-pass':
                    filtered_row =  butter_lowpass_filter(signal=row, cutoff=btt_co, fs=btt_sf, 
                                                       order=btt_or, show=show, stream=show)
                elif btt_type == 'band-pass':
                    filtered_row = butter_bandpass_filter(signal=row, lowcut=btt_lc, highcut=btt_hc,
                                                       fs=btt_sf, order=btt_or, show=show, stream=show)
                elif btt_type == 'band-stop':
                    filtered_row = butter_bandstop_filter(signal=row, lowcut=btt_lc, highcut=btt_hc,
                                                       fs=btt_sf, order=btt_or, show=show, stream=show)
                #my_stft(row, plot=show, fs=2, stream=show)
                #my_stft(filtered_row, plot=show, fs=2, stream=show)
                filtered_signal[pr_count] = filtered_row
                pr_count += 1
    
            active_save_verification(filtered_signal)

if dsp_box == 'filtering':
    if filter_box == 'adaptive':
        adpt_n = st.sidebar.number_input(label='order',min_value=1,step=1,value=100, key="adaptive_order")
        adpt_mu = st.sidebar.number_input(label='convergence factor',min_value=1,step=1,value=5, key="adaptive_convergence_factor")
        
if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'filtering':
    if filter_box == 'adaptive':
        if st.sidebar.button("Filter Signal with Adaptive"):
            filtered_signal = st.session_state["active_dataset"].copy()
            ad_count = 0
            for row in filtered_signal:
                if ad_count == 0:
                    show = True
                else:
                    show = False
                filtered_row, error, weight = lms_filter(x=noise_template, d=row, n=adpt_n, mu=adpt_mu, show=show, stream=show)
                filtered_new = row - filtered_row
                filtered_signal[ad_count] = filtered_new
                ad_count += 1
    
            active_save_verification(filtered_signal)



wavelet_tuple = ('haar', 'dmey')

if dsp_box == 'filtering':
    if filter_box == 'denoising':
        dns_type = st.sidebar.selectbox('**Select the type of filtering.**', denoise_tuple)
        
        dns_th = st.sidebar.number_input(label='threshold',min_value=1,step=1,value=5, key="denoising_threshold")

        if dns_type == 'wavelet':
            dns_mt = st.sidebar.selectbox('Select Wavelet Method.', wavelet_tuple)
        
if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'filtering':
    if filter_box == 'denoising':
        if st.sidebar.button("Denoise Signal"):
            filtered_signal = st.session_state["active_dataset"].copy()
            pr_count = 0
            for row in filtered_signal:
                if pr_count == 0:
                    show = True
                else:
                    show = False
                if dns_type == 'fft':
                    filtered_row = fft_denoise(signal=row, threshold=dns_th, show=show, stream=show)
                elif dns_type == 'wavelet':
                    filtered_row =  wavelet_denoise(data=row, method=dns_mt, threshold=dns_th, show=show, 
                                                    title="Wavelet Denoising", stream=show)
                filtered_signal[pr_count] = filtered_row
                pr_count += 1
    
            active_save_verification(filtered_signal)


if dsp_box == 'filtering':
    if filter_box == 'kalman':
      
        kal_xl = st.sidebar.number_input(label='x_last',min_value=0,step=1,value=0, key="kalman_x_last")
        kal_pl = st.sidebar.number_input(label='p_last',min_value=0,step=1,value=0, key="kalman_p_last")
        kal_q = st.sidebar.number_input(label='Q',step=0.01,format="%.02f",value=0.1, key="kalman_q")
        kal_r = st.sidebar.number_input(label='R',step=0.01,format="%.02f",value=0.1, key='kalman_r')
        
if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'filtering':
    if filter_box == 'kalman':
        if st.sidebar.button("Filter Signal with Kalman"):
            filtered_signal = st.session_state["active_dataset"].copy()
            pr_count = 0
            for row in filtered_signal:
                if pr_count == 0:
                    show = True
                else:
                    show = False
                filtered_row =  kalman_filter(x=row, x_last=kal_xl, p_last=kal_pl, Q=kal_q, R=kal_r, show=show, stream=show)
                filtered_signal[pr_count] = filtered_row
                pr_count += 1
    
            active_save_verification(filtered_signal)

##########################################################
# TIME & FREQUENCY DOMAIN FEATURES
##########################################################
            
time_freq_tuple = ('time domain features', 'peaks & envelopes', 'power spectral density', 'transforms', 'misc')

#td_tuple = ('statistical moments', 'petrosian fractal dimension')
if dsp_box == 'time & frequency domain features':
    time_freq_box = st.sidebar.selectbox('**Select the features to extract.**', time_freq_tuple)

if dsp_box == 'time & frequency domain features':
    if time_freq_box == 'time domain features':
      
        pmu_check = st.sidebar.checkbox("PMU (frequency, amplitude, phase angle)",key="pmu check")
        if pmu_check == True:
            pmu_sf = st.sidebar.number_input(label='pmu sampling frequency',min_value=1,step=1,value=1, key="pmu_sampline_frequency")
        mean_check = st.sidebar.checkbox("Mean",key="mean check")
        var_check = st.sidebar.checkbox("Variance",key="variance check")
        skew_check = st.sidebar.checkbox("Skewness",key="skewness check")
        kurt_check = st.sidebar.checkbox("Kurtosis",key="kurtosis check")
        pfd_check = st.sidebar.checkbox("Petrosian Fractal Dimension",key="pfd check")
        thd_check = st.sidebar.checkbox("Total Harmonic Distortion",key="thd check")
        if thd_check == True:
            thd_fund = st.sidebar.number_input(label='fundamental frequency',min_value=1,step=1,value=1, key="thd_fundamental_frequency")
            thd_sf = st.sidebar.number_input(label='thd sampling frequency',min_value=2,step=1,value=2, key="thd_sampling_frequency")
            thd_har = st.sidebar.number_input(label='number of harmonics',min_value=1,step=1,value=5, key="thd_number_harmonics")
        
        if pmu_check == True or mean_check == True or var_check == True or skew_check == True or kurt_check == True or pfd_check == True or thd_check == True:
            any_checked = True
        else:
            any_checked = False

        
if not str(st.session_state["active_dataset"]) == "" and dsp_box == 'time & frequency domain features' and any_checked == True:
    if time_freq_box == 'time domain features':
        if st.sidebar.button("Extract Features"):
            current_signal = st.session_state["active_dataset"].copy()
            ex_count = 0
            extracted_list = []            
            first_row_info = []
            for row in current_signal:  
                current_list = []              
                if pmu_check == True:
                    pmu_tuple = extract_pmu(row, pmu_sf)
                    current_list.append(pmu_tuple[0])
                    current_list.append(pmu_tuple[1])
                    current_list.append(pmu_tuple[2])
                    if ex_count == 0:
                        freq_txt = "The Frequency is " + str(pmu_tuple[0])
                        first_row_info.append(freq_txt)
                        amp_txt = "The Amplitude is " + str(pmu_tuple[1])
                        first_row_info.append(amp_txt)
                        phas_txt = "The Phase Angle is " + str(pmu_tuple[2])
                        first_row_info.append(phas_txt)
                if mean_check == True:
                    cur_mean = np.mean(row)
                    current_list.append(cur_mean)
                    if ex_count == 0:
                        mean_txt = "The Mean is " + str(cur_mean)
                        first_row_info.append(mean_txt)
                if var_check == True:
                    cur_var = np.var(row)
                    current_list.append(cur_var)
                    if ex_count == 0:
                        var_txt = "The Variance is " + str(cur_var)
                        first_row_info.append(var_txt)
                if skew_check == True:
                    cur_skew = skew(row)
                    current_list.append(cur_skew)
                    if ex_count == 0:
                        skew_txt = "The Skewness is " + str(cur_skew)
                        first_row_info.append(skew_txt)
                if kurt_check == True:
                    cur_kurt = kurtosis(row)
                    current_list.append(cur_kurt)
                    if ex_count == 0:
                        kurt_txt = "The Kurtosis is " + str(cur_kurt)
                        first_row_info.append(kurt_txt)
                if pfd_check == True:
                    cur_pfd = pfd(row)
                    current_list.append(cur_pfd)
                    if ex_count == 0:
                        pfd_txt = "Petrosian Fractal Dimension " + str(cur_pfd)
                        first_row_info.append(pfd_txt)
                if thd_check == True:
                    cur_thd = calculate_thd(row, thd_fund, thd_sf, thd_har)
                    current_list.append(cur_thd)
                    if ex_count == 0:
                        thd_txt = "The Total Harmonic Distortion is " + str(cur_thd)
                        first_row_info.append(thd_txt)
                
                #current_array = np.array(current_list)
                if ex_count == 0:
                    st.write("THE EXTRACTED FEATURES FOR THE FIRST INPUT SIGNAL ARE:")
                    for item in first_row_info:
                        st.write(item)

                extracted_list.append(current_list)

                ex_count += 1

            extracted_signal = np.array(extracted_list)

            df = pd.DataFrame(extracted_signal)
            st.title("Feature Preview")
            st.dataframe(df.head(5))
            active_save_verification(extracted_signal)

##########################################################
# SIGNAL DECOMPOSITION
##########################################################
            
decomp_tuple = ('')



##########################################################
# TRANSFORMS
##########################################################



##########################################################
# WAVELET ANALYSIS
##########################################################
            


