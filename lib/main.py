import tkinter
import customtkinter
import yaml
import threading
from pathlib import Path
from utils import run_script, data_loader_confg
from data_gui import *
from classification_gui import *

current_dir = Path.cwd() # assumes your working directory is in "SensorwebAiFramework"

ftype_npy = [("npy files","*.npy")]
ftype_yaml = [("yaml files","*.yaml")]

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


device = None
model = None
# Open File Dialog
def select_yaml_file(button_name = None, tab = None):
    global device
    global model
    global active_tab
    filename = customtkinter.filedialog.askopenfilename(filetypes=ftype_yaml)
    if button_name == "select_device":
        if tab == 'tab_6':
            select_device.configure(text = filename)                       
        elif tab == 'tab_7':
            select_historical.configure(text = filename)
        device = filename
        active_tab = tab 
    elif button_name == "select_model":
        if tab == 'tab_6':
            select_model.configure(text = filename)
        elif tab == 'tab_7':
            select_model7.configure(text = filename)
        model = filename
        active_tab = tab 
    
    if (device != None) and (model != None) and (".yaml" in device) and (".yaml" in model):
        if active_tab == 'tab_6':
            start_connection.configure(state="normal")
        elif active_tab == "tab_7":
            start_historical.configure(state="normal")

    return filename

# Method to connect model to smart device
def connect_model_to_device(device_name,model_name):
    global conn_script
    global stop_event
    print("Connecting - model: ",model_name,"To device: ",device_name)

    stop_event = threading.Event()
    script_path = current_dir / "mqtt/main_ai_mqtt.py"
    arguments = [device_name, model_name]

    conn_script = threading.Thread(target=run_script, args=(script_path, arguments, stop_event))
    conn_script.start()

    start_connection.configure(state="disabled")
    stop_connection.configure(state="normal")


# Method to disconnect model from device
def disconnect_model_from_device(device_name,model_name):
    global conn_script
    global device
    global model
    global stop_event
    global active_tab
    #conn_script.stop()
    stop_event.set()
    conn_script.join()
    print("Thread terminated.")
    select_device.configure(text = "select device yaml")
    select_model.configure(text = "select model yaml")
    device = None
    model = None
    start_connection.configure(state="disabled")
    stop_connection.configure(state = "disabled")
    active_tab = None

# Method to connect to db
def connect_model_to_db(device_name,model_name):
    global conn_script
    global stop_event
    print("Connecting - model: ",model_name,"To device: ",device_name)

    stop_event = threading.Event()
    script_path = current_dir / "mqtt/main_ai_influx.py"
    arguments = [device_name, model_name]

    conn_script = threading.Thread(target=run_script, args=(script_path, arguments, stop_event))
    conn_script.start()

    start_historical.configure(state="disabled")

    stop_historical.configure(state="normal")

# Method to disconnect from db
def disconnect_model_from_db(device_name,model_name):
    global conn_script
    global device
    global model
    global stop_event
    global active_tab
    #conn_script.stop()
    stop_event.set()
    conn_script.join()
    print("Thread terminated.")
    select_historical.configure(text = "select device yaml")
    select_model7.configure(text = "select model yaml")
    device = None
    model = None
    start_historical.configure(state="disabled")
    stop_historical.configure(state = "disabled")
    active_tab=None

#root = Tk()
root = customtkinter.CTk()

root.title("Sensor AI")
#root.inconbitmap("images/codemy.ico")
root.geometry("850x400")

# Ensure data configuration set to default
data_loader_confg()

# create Tabview
main_tab = customtkinter.CTkTabview(root,
                                  width=700,
                                  height=350,
                                  corner_radius=10)
main_tab.pack(pady=10)

# Create tabs
tab_0 = main_tab.add("Data")
tab_1 = main_tab.add("DSP")
tab_2 = main_tab.add("Classification")
tab_3 = main_tab.add("Clustering")
tab_4 = main_tab.add("Detection")
tab_5 = main_tab.add("Regression")
tab_6 = main_tab.add("Device Connector")
tab_7 = main_tab.add("Historical Data Connector")

# create dsp tabview
dsp_tab = customtkinter.CTkTabview(tab_1,
                                  width=650,
                                  height=30,
                                  corner_radius=10)
dsp_tab.pack(pady=10)

# Create dsp subtabs
tab_noise = dsp_tab.add("Noise")
tab_filters = dsp_tab.add("Filters")
tab_decomp = dsp_tab.add("Decomposition")
tab_time = dsp_tab.add("Time Domain Features")
tab_trans = dsp_tab.add("Transforms")
tab_misc = dsp_tab.add("Misc")

# create detection tabview
detection_tab = customtkinter.CTkTabview(tab_4,
                                  width=650,
                                  height=30,
                                  corner_radius=10)
detection_tab.pack(pady=10)

# Create detection tabs
tab_nov = detection_tab.add("Novelty")
tab_out = detection_tab.add("Outlier")


#############################################################
# TAB 0 - DATA
#############################################################

load_datafile_button = customtkinter.CTkButton(tab_0, text="load data from .npy file", command=open_data_loader_window)
load_datafile_button.grid(row=0,column=0,padx=10, pady=10)

generate_wavedata_button = customtkinter.CTkButton(tab_0, text="generate waveform dataset", command=generate_wavedata_window_opener)
generate_wavedata_button.grid(row=1,column=0,padx=10, pady=10)

generate_scgdata_button = customtkinter.CTkButton(tab_0, text="generate scg dataset", command=generate_scg_window_opener)
generate_scgdata_button.grid(row=2,column=0,padx=10, pady=10)

x_train_data = customtkinter.CTkLabel(tab_0, text="Training Data: None Selected")
x_train_data.grid(row=0,column=2,padx=10, pady=10)

y_train_labels = customtkinter.CTkLabel(tab_0, text="Training Labels: None Selected")
y_train_labels.grid(row=1,column=2,padx=10, pady=10)

x_test_data = customtkinter.CTkLabel(tab_0, text="Test Data: None Selected!")
x_test_data.grid(row=2,column=2,padx=10, pady=10)

y_test_labels = customtkinter.CTkLabel(tab_0, text="Test Labels: : None Selected")
y_test_labels.grid(row=3,column=2,padx=10, pady=10)



#############################################################
# TAB 1 - DSP
#############################################################

# Noise Tab

white_noise_button = customtkinter.CTkButton(tab_noise, text="white", command=open_decision_tree_window)
white_noise_button.grid(row=0,column=0,padx=10, pady=10)

bl_white_noise_button = customtkinter.CTkButton(tab_noise, text="band limited white", command=open_decision_tree_window)
bl_white_noise_button.grid(row=1,column=0,padx=10, pady=10)

impulse_noise_button = customtkinter.CTkButton(tab_noise, text="impulse", command=open_decision_tree_window)
impulse_noise_button.grid(row=2,column=0,padx=10, pady=10)

burst_noise_button = customtkinter.CTkButton(tab_noise, text="burst", command=open_decision_tree_window)
burst_noise_button.grid(row=0,column=1,padx=10, pady=10)

brown_noise_button = customtkinter.CTkButton(tab_noise, text="brown", command=open_decision_tree_window)
brown_noise_button.grid(row=1,column=1,padx=10, pady=10)

pink_noise_button = customtkinter.CTkButton(tab_noise, text="pink", command=open_decision_tree_window)
pink_noise_button.grid(row=2,column=1,padx=10, pady=10)

flicker_noise_button = customtkinter.CTkButton(tab_noise, text="flicker", command=open_decision_tree_window)
flicker_noise_button.grid(row=0,column=2,padx=10, pady=10)

powerline_noise_button = customtkinter.CTkButton(tab_noise, text="powerline", command=open_decision_tree_window)
powerline_noise_button.grid(row=1,column=2,padx=10, pady=10)

resonance_noise_button = customtkinter.CTkButton(tab_noise, text="resonance", command=open_decision_tree_window)
resonance_noise_button.grid(row=2,column=2,padx=10, pady=10)

# Filters Tab

lowpass_button = customtkinter.CTkButton(tab_filters, text="low pass", command=open_decision_tree_window)
lowpass_button.grid(row=0,column=0,padx=10, pady=10)

highpass_button = customtkinter.CTkButton(tab_filters, text="high pass", command=open_decision_tree_window)
highpass_button.grid(row=1,column=0,padx=10, pady=10)

bandpass_button = customtkinter.CTkButton(tab_filters, text="band pass", command=open_decision_tree_window)
bandpass_button.grid(row=2,column=0,padx=10, pady=10)

bandstop_button = customtkinter.CTkButton(tab_filters, text="band stop", command=open_decision_tree_window)
bandstop_button.grid(row=3,column=0,padx=10, pady=10)

kalman_button = customtkinter.CTkButton(tab_filters, text="kalman", command=open_decision_tree_window)
kalman_button.grid(row=0,column=1,padx=10, pady=10)

matched_button = customtkinter.CTkButton(tab_filters, text="matched", command=open_decision_tree_window)
matched_button.grid(row=1,column=1,padx=10, pady=10)

notch_button = customtkinter.CTkButton(tab_filters, text="notch", command=open_decision_tree_window)
notch_button.grid(row=2,column=1,padx=10, pady=10)

wiener_button = customtkinter.CTkButton(tab_filters, text="weiner", command=open_decision_tree_window)
wiener_button.grid(row=3,column=1,padx=10, pady=10)

adaptive_button = customtkinter.CTkButton(tab_filters, text="adaptive", command=open_decision_tree_window)
adaptive_button.grid(row=0,column=2,padx=10, pady=10)

savgol_button = customtkinter.CTkButton(tab_filters, text="savitzky-golay", command=open_decision_tree_window)
savgol_button.grid(row=1,column=2,padx=10, pady=10)

fft_denoising_button = customtkinter.CTkButton(tab_filters, text="fft denoising", command=open_decision_tree_window)
fft_denoising_button.grid(row=0,column=3,padx=10, pady=10)

wavelet_denoising_button = customtkinter.CTkButton(tab_filters, text="wavelet denoising", command=open_decision_tree_window)
wavelet_denoising_button.grid(row=1,column=3,padx=10, pady=10)

# Decomposition Tab

seasonal_button = customtkinter.CTkButton(tab_decomp, text="seasonal", command=open_decision_tree_window)
seasonal_button.grid(row=0,column=0,padx=10, pady=10)

emd_button = customtkinter.CTkButton(tab_decomp, text="emperical mode", command=open_decision_tree_window)
emd_button.grid(row=0,column=1,padx=10, pady=10)

eemd_button = customtkinter.CTkButton(tab_decomp, text="ensemble emd", command=open_decision_tree_window)
eemd_button.grid(row=1,column=1,padx=10, pady=10)

ceemd_button = customtkinter.CTkButton(tab_decomp, text="complete eemd", command=open_decision_tree_window)
ceemd_button.grid(row=2,column=1,padx=10, pady=10)

vmd_button = customtkinter.CTkButton(tab_decomp, text="variational mode", command=open_decision_tree_window)
vmd_button.grid(row=0,column=2,padx=10, pady=10)

pca_blind_button = customtkinter.CTkButton(tab_decomp, text="pca blind source", command=open_decision_tree_window)
pca_blind_button.grid(row=0,column=3,padx=10, pady=10)

ica_blind_button = customtkinter.CTkButton(tab_decomp, text="ica blind source", command=open_decision_tree_window)
ica_blind_button.grid(row=1,column=3,padx=10, pady=10)

# Time Domain Tab

peaks_button = customtkinter.CTkButton(tab_time, text="peak of peak", command=open_decision_tree_window)
peaks_button.grid(row=0,column=0,padx=10, pady=10)

envelope_button = customtkinter.CTkButton(tab_time, text="envelope from peaks", command=open_decision_tree_window)
envelope_button.grid(row=1,column=0,padx=10, pady=10)

average_env_button = customtkinter.CTkButton(tab_time, text="average envelope", command=open_decision_tree_window)
average_env_button.grid(row=2,column=0,padx=10, pady=10)

pfd_button = customtkinter.CTkButton(tab_time, text="petrosian fractal dimension", command=open_decision_tree_window)
pfd_button.grid(row=0,column=1,padx=10, pady=10)

mean_button = customtkinter.CTkButton(tab_time, text="mean", command=open_decision_tree_window)
mean_button.grid(row=0,column=2,padx=10, pady=10)

variance_button = customtkinter.CTkButton(tab_time, text="variance", command=open_decision_tree_window)
variance_button.grid(row=1,column=2,padx=10, pady=10)

skewness_button = customtkinter.CTkButton(tab_time, text="skewness", command=open_decision_tree_window)
skewness_button.grid(row=2,column=2,padx=10, pady=10)

kurtosis_button = customtkinter.CTkButton(tab_time, text="kurtosis", command=open_decision_tree_window)
kurtosis_button.grid(row=3,column=2,padx=10, pady=10)

# Transforms Tab

fft_button = customtkinter.CTkButton(tab_trans, text="fft", command=open_decision_tree_window)
fft_button.grid(row=0,column=0,padx=10, pady=10)

psd_button = customtkinter.CTkButton(tab_trans, text="power spectral density", command=open_decision_tree_window)
psd_button.grid(row=1,column=0,padx=10, pady=10)

stft_button = customtkinter.CTkButton(tab_trans, text="short time ft", command=open_decision_tree_window)
stft_button.grid(row=2,column=0,padx=10, pady=10)

wavelet_button = customtkinter.CTkButton(tab_trans, text="wavelet", command=open_decision_tree_window)
wavelet_button.grid(row=0,column=1,padx=10, pady=10)

chirplet_button = customtkinter.CTkButton(tab_trans, text="chirplet", command=open_decision_tree_window)
chirplet_button.grid(row=1,column=1,padx=10, pady=10)

hilbert_button = customtkinter.CTkButton(tab_trans, text="hilbert", command=open_decision_tree_window)
hilbert_button.grid(row=0,column=2,padx=10, pady=10)

synchro_squeeze_button = customtkinter.CTkButton(tab_trans, text="synchro-squeezing", command=open_decision_tree_window)
synchro_squeeze_button.grid(row=1,column=2,padx=10, pady=10)

wigner_button = customtkinter.CTkButton(tab_trans, text="wigner ville dist", command=open_decision_tree_window)
wigner_button.grid(row=2,column=2,padx=10, pady=10)

#############################################################
# TAB 2 - CLASSIFICATION
#############################################################

# Tree based models
decision_tree_button = customtkinter.CTkButton(tab_2, text="decision tree", command=open_decision_tree_window)
decision_tree_button.grid(row=0,column=0,padx=10, pady=10)

extra_trees_button = customtkinter.CTkButton(tab_2, text="extra trees", command=open_extra_trees_window)
extra_trees_button.grid(row=1,column=0,padx=10, pady=10)

random_forest_button = customtkinter.CTkButton(tab_2, text="random forest", command=open_random_forest_window)
random_forest_button.grid(row=2,column=0,padx=10, pady=10)

gradient_boosting_button = customtkinter.CTkButton(tab_2, text="gradient boosting", command=open_decision_tree_window)
gradient_boosting_button.grid(row=3,column=0,padx=10, pady=10)

# Nearest neighbor based models
knn_button = customtkinter.CTkButton(tab_2, text="k nearest neighbors", command=open_decision_tree_window)
knn_button.grid(row=0,column=1,padx=10, pady=10)

nearest_centroid_button = customtkinter.CTkButton(tab_2, text="nearest centroid", command=open_decision_tree_window)
nearest_centroid_button.grid(row=1,column=1,padx=10, pady=10)

radius_nn_button = customtkinter.CTkButton(tab_2, text="radius nearest neighbors", command=open_decision_tree_window)
radius_nn_button.grid(row=2,column=1,padx=10, pady=10)

ts_knn_button = customtkinter.CTkButton(tab_2, text="time series knn", command=open_decision_tree_window)
ts_knn_button.grid(row=3,column=1,padx=10, pady=10)

# Support Vector based models

svc_button = customtkinter.CTkButton(tab_2, text="support vector", command=open_decision_tree_window)
svc_button.grid(row=0,column=2,padx=10, pady=10)

nu_svc_button = customtkinter.CTkButton(tab_2, text="nu support vector", command=open_decision_tree_window)
nu_svc_button.grid(row=1,column=2,padx=10, pady=10)

ts_svc_button = customtkinter.CTkButton(tab_2, text="time series svc", command=open_decision_tree_window)
ts_svc_button.grid(row=2,column=2,padx=10, pady=10)

# Function Buttons
reset_class_queue_button = customtkinter.CTkButton(tab_2, text="reset queue", command=reset_class_queue,
                                                  fg_color='red',
                                                  hover_color='pink')
reset_class_queue_button.grid(row=9,column=2,padx=10, pady=10)

show_class_queue_button = customtkinter.CTkButton(tab_2, text="show queue", command=show_class_queue,
                                                  fg_color='red',
                                                  hover_color='pink')
show_class_queue_button.grid(row=9,column=3,padx=10, pady=10)

class_gridsearch_button = customtkinter.CTkButton(tab_2, text="run class gridsearch", command=execute_class_gridsearch,
                                                  fg_color='red',
                                                  hover_color='pink')
class_gridsearch_button.grid(row=9,column=4,padx=10, pady=10)


#############################################################
# TAB 3 - CLUSTERING
#############################################################

# Hierarchical base algorithms
affin_prop_button = customtkinter.CTkButton(tab_3, text="affinity propagation", command=open_decision_tree_window)
affin_prop_button.grid(row=0,column=0,padx=10, pady=10)

# density based algorithms
dbscan_button = customtkinter.CTkButton(tab_3, text="dbscan", command=open_decision_tree_window)
dbscan_button.grid(row=0,column=1,padx=10, pady=10)

optics_button = customtkinter.CTkButton(tab_3, text="optics", command=open_decision_tree_window)
optics_button.grid(row=1,column=1,padx=10, pady=10)

mean_shift_button = customtkinter.CTkButton(tab_3, text="mean shift", command=open_decision_tree_window)
mean_shift_button.grid(row=2,column=1,padx=10, pady=10)

# k means based algorithms

kmeans_button = customtkinter.CTkButton(tab_3, text="k means", command=open_decision_tree_window)
kmeans_button.grid(row=0,column=2,padx=10, pady=10)

bi_kmeans_button = customtkinter.CTkButton(tab_3, text="bisecting k means", command=open_decision_tree_window)
bi_kmeans_button.grid(row=1,column=2,padx=10, pady=10)

mini_kmeans_button = customtkinter.CTkButton(tab_3, text="mini-batch k means", command=open_decision_tree_window)
mini_kmeans_button.grid(row=2,column=2,padx=10, pady=10)

ts_kmeans_button = customtkinter.CTkButton(tab_3, text="time series k means", command=open_decision_tree_window)
ts_kmeans_button.grid(row=3,column=2,padx=10, pady=10)

# Spectral based algorithms
spectral_button= customtkinter.CTkButton(tab_3, text="spectral clustering", command=open_decision_tree_window)
spectral_button.grid(row=0,column=3,padx=10, pady=10)

# Function Buttons
reset_clust_queue_button = customtkinter.CTkButton(tab_2, text="reset queue", command=reset_clust_queue,
                                                  fg_color='red',
                                                  hover_color='pink')
reset_clust_queue_button.grid(row=9,column=2,padx=10, pady=10)

show_clust_queue_button = customtkinter.CTkButton(tab_2, text="show queue", command=show_clust_queue,
                                                  fg_color='red',
                                                  hover_color='pink')
show_clust_queue_button.grid(row=9,column=3,padx=10, pady=10)

clust_gridsearch_button = customtkinter.CTkButton(tab_2, text="run class gridsearch", command=execute_clust_gridsearch,
                                                  fg_color='red',
                                                  hover_color='pink')
clust_gridsearch_button.grid(row=9,column=4,padx=10, pady=10)

#############################################################
# TAB 4 - DETECTION
#############################################################

# Novelty Detection
lof_nov_button= customtkinter.CTkButton(tab_nov, text="local outlier factor", command=open_decision_tree_window)
lof_nov_button.pack(padx=10, pady=10)

# Outlier Detection
lof_out_button = customtkinter.CTkButton(tab_out, text="local outlier factor", command=open_decision_tree_window)
lof_out_button.pack(padx=10, pady=10)

iso_forest_button = customtkinter.CTkButton(tab_out, text="isolation forest", command=open_decision_tree_window)
iso_forest_button.pack(padx=10, pady=10)


#############################################################
# TAB 5 - REGRESSION
#############################################################

# Linear models
linear_button = customtkinter.CTkButton(tab_5, text="linear", command=open_decision_tree_window)
linear_button.grid(row=0,column=0,padx=10, pady=10)

gamma_button = customtkinter.CTkButton(tab_5, text="gamma", command=open_decision_tree_window)
gamma_button.grid(row=1,column=0,padx=10, pady=10)

poisson_button = customtkinter.CTkButton(tab_5, text="poisson", command=open_decision_tree_window)
poisson_button.grid(row=2,column=0,padx=10, pady=10)

tweedie_button = customtkinter.CTkButton(tab_5, text="tweedie", command=open_decision_tree_window)
tweedie_button.grid(row=3,column=0,padx=10, pady=10)

# Lars / Lasso based models
lars_cv_button = customtkinter.CTkButton(tab_5, text="lars", command=open_decision_tree_window)
lars_cv_button.grid(row=0,column=1,padx=10, pady=10)

lasso_cv_button = customtkinter.CTkButton(tab_5, text="lasso", command=open_decision_tree_window)
lasso_cv_button.grid(row=1,column=1,padx=10, pady=10)

lasso_lars_cv_button = customtkinter.CTkButton(tab_5, text="lasso-lars", command=open_decision_tree_window)
lasso_lars_cv_button.grid(row=2,column=1,padx=10, pady=10)

lasso_lars_ic_button = customtkinter.CTkButton(tab_5, text="lasso-lars w/ info criteria", command=open_decision_tree_window)
lasso_lars_ic_button.grid(row=3,column=1,padx=10, pady=10)

# Ridge based models
ridge_cv_button = customtkinter.CTkButton(tab_5, text="ridge", command=open_decision_tree_window)
ridge_cv_button.grid(row=0,column=2,padx=10, pady=10)

bays_ridge_button = customtkinter.CTkButton(tab_5, text="baesian ridge", command=open_decision_tree_window)
bays_ridge_button.grid(row=1,column=2,padx=10, pady=10)

# Elastic nets
enet_cv_button = customtkinter.CTkButton(tab_5, text="elastic net", command=open_decision_tree_window)
enet_cv_button.grid(row=0,column=3,padx=10, pady=10)

# Quantile
quantile_button = customtkinter.CTkButton(tab_5, text="quantile", command=open_decision_tree_window)
quantile_button.grid(row=1,column=3,padx=10, pady=10)

# Support vector based models
svr_button = customtkinter.CTkButton(tab_5, text="support vector", command=open_decision_tree_window)
svr_button.grid(row=0,column=4,padx=10, pady=10)

lin_svr_button = customtkinter.CTkButton(tab_5, text="linear svr", command=open_decision_tree_window)
lin_svr_button.grid(row=1,column=4,padx=10, pady=10)

nu_svr_button = customtkinter.CTkButton(tab_5, text="nu svr", command=open_decision_tree_window)
nu_svr_button.grid(row=2,column=4,padx=10, pady=10)

ts_svr_button = customtkinter.CTkButton(tab_5, text="time series svr", command=open_decision_tree_window)
ts_svr_button.grid(row=3,column=4,padx=10, pady=10)

#############################################################
# TAB 6 - DEVICE CONNECTOR
#############################################################
select_device = customtkinter.CTkButton(tab_6,text="select device yaml",command=lambda: select_yaml_file("select_device","tab_6"))
select_device.pack(pady=10)

select_model = customtkinter.CTkButton(tab_6,text="select model yaml",command=lambda: select_yaml_file("select_model","tab_6"))
select_model.pack(pady=10)

start_connection = customtkinter.CTkButton(tab_6,text="start the connection",state="disabled" ,command=lambda: connect_model_to_device(device_name=device,model_name=model))
start_connection.pack(pady=10)

stop_connection = customtkinter.CTkButton(tab_6,text="stop the connection",state="disabled" ,command=lambda: disconnect_model_from_device(device_name=device,model_name=model))
stop_connection.pack(pady=10)

#############################################################
# TAB 7 - HISTORICAL DATA
#############################################################
select_historical = customtkinter.CTkButton(tab_7,text="select device yaml",command=lambda: select_yaml_file("select_device","tab_7"))
select_historical.pack(pady=10)

select_model7 = customtkinter.CTkButton(tab_7,text="select model yaml",command=lambda: select_yaml_file("select_model","tab_7"))
select_model7.pack(pady=10)

start_historical = customtkinter.CTkButton(tab_7,text="start db download",state="disabled" ,command=lambda: connect_model_to_db(device_name=device,model_name=model))
start_historical.pack(pady=10)

stop_historical = customtkinter.CTkButton(tab_7,text="end db connection",state="disabled" ,command=lambda: disconnect_model_from_db(device_name=device,model_name=model))
stop_historical.pack(pady=10)

# Run app
root.mainloop()