import tkinter
import customtkinter
import yaml
import threading
from pathlib import Path
from utils import run_script, data_loader_confg
from data_gui import *
from classification_gui import *

global current_dataset
global current_labels
global current_model_queue

current_dataset = None
current_labels = None
current_model_queue = []

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
root.geometry("800x400")

# Ensure data configuration set to default
data_loader_confg()

# create Tabview
my_tab = customtkinter.CTkTabview(root,
                                  width=700,
                                  height=350,
                                  corner_radius=10)
my_tab.pack(pady=10)

# Create tabs
tab_0 = my_tab.add("Data")
tab_1 = my_tab.add("DSP")
tab_2 = my_tab.add("Classification")
tab_3 = my_tab.add("Clustering")
tab_4 = my_tab.add("Detection")
tab_5 = my_tab.add("Regression")
tab_6 = my_tab.add("Device Connector")
tab_7 = my_tab.add("Historical Data Connector")


#############################################################
# TAB 0 - DATA
#############################################################

load_datafile_button = customtkinter.CTkButton(tab_0, text="load data from .npy file", command=open_data_loader_window)
load_datafile_button.pack(padx=20, pady=20)

generate_wavedata_button = customtkinter.CTkButton(tab_0, text="generate waveform dataset", command=generate_wavedata_window_opener)
generate_wavedata_button.pack(padx=20, pady=20)

generate_scgdata_button = customtkinter.CTkButton(tab_0, text="generate scg dataset", command=generate_scg_window_opener)
generate_scgdata_button.pack(padx=20, pady=20)

#############################################################
# TAB 1 - DSB
#############################################################


#############################################################
# TAB 2 - CLASSIFICATION
#############################################################

# Tree based models
decision_tree_button = customtkinter.CTkButton(tab_2, text="decision tree", command=open_decision_tree_window)
decision_tree_button.pack(padx=10, pady=10)

extra_trees_button = customtkinter.CTkButton(tab_2, text="extra trees", command=open_decision_tree_window)
extra_trees_button.pack(padx=10, pady=10)

random_forest_button = customtkinter.CTkButton(tab_2, text="random forest", command=open_decision_tree_window)
random_forest_button.pack(padx=10, pady=10)

gradient_boosting_button = customtkinter.CTkButton(tab_2, text="gradient boosting", command=open_decision_tree_window)
gradient_boosting_button.pack(padx=10, pady=10)

# Nearest neighbor based models
knn_button = customtkinter.CTkButton(tab_2, text="k nearest neighbors", command=open_decision_tree_window)
knn_button.pack(padx=10, pady=10)

nearest_centroid_button = customtkinter.CTkButton(tab_2, text="nearest centroid", command=open_decision_tree_window)
nearest_centroid_button.pack(padx=10, pady=10)

radius_nn_button = customtkinter.CTkButton(tab_2, text="radius nearest neighbors", command=open_decision_tree_window)
radius_nn_button.pack(padx=10, pady=10)

ts_knn_button = customtkinter.CTkButton(tab_2, text="time series knn", command=open_decision_tree_window)
ts_knn_button.pack(padx=10, pady=10)

# Support Vector based models

svc_button = customtkinter.CTkButton(tab_2, text="support vector", command=open_decision_tree_window)
svc_button.pack(padx=10, pady=10)

nu_svc_button = customtkinter.CTkButton(tab_2, text="nu support vector", command=open_decision_tree_window)
nu_svc_button.pack(padx=10, pady=10)

ts_svc_button = customtkinter.CTkButton(tab_2, text="time series svc", command=open_decision_tree_window)
ts_svc_button.pack(padx=10, pady=10)

#############################################################
# TAB 3 - CLUSTERING
#############################################################

# Hierarchical base algorithms
affin_prop_button = customtkinter.CTkButton(tab_3, text="affinity propagation", command=open_decision_tree_window)
affin_prop_button.pack(padx=10, pady=10)

# density based algorithms
dbscan_button = customtkinter.CTkButton(tab_3, text="dbscan", command=open_decision_tree_window)
dbscan_button.pack(padx=10, pady=10)

optics_button = customtkinter.CTkButton(tab_3, text="optics", command=open_decision_tree_window)
optics_button.pack(padx=10, pady=10)

mean_shift_button = customtkinter.CTkButton(tab_3, text="mean shift", command=open_decision_tree_window)
mean_shift_button.pack(padx=10, pady=10)

# k means based algorithms

kmeans_button = customtkinter.CTkButton(tab_3, text="k means", command=open_decision_tree_window)
kmeans_button.pack(padx=10, pady=10)

bi_kmeans_button = customtkinter.CTkButton(tab_3, text="bisecting k means", command=open_decision_tree_window)
bi_kmeans_button.pack(padx=10, pady=10)

mini_kmeans_button = customtkinter.CTkButton(tab_3, text="mini-batch k means", command=open_decision_tree_window)
mini_kmeans_button.pack(padx=10, pady=10)

ts_kmeans_button = customtkinter.CTkButton(tab_3, text="time series k means", command=open_decision_tree_window)
ts_kmeans_button.pack(padx=10, pady=10)

# Spectral based algorithms
spectral_button= customtkinter.CTkButton(tab_3, text="spectral clustering", command=open_decision_tree_window)
spectral_button.pack(padx=10, pady=10)

#############################################################
# TAB 4 - DETECTION
#############################################################



#############################################################
# TAB 5 - REGRESSION
#############################################################

# Linear models
linear_button = customtkinter.CTkButton(tab_5, text="linear", command=open_decision_tree_window)
linear_button.pack(padx=10, pady=10)

gamma_button = customtkinter.CTkButton(tab_5, text="gamma", command=open_decision_tree_window)
gamma_button.pack(padx=10, pady=10)

poisson_button = customtkinter.CTkButton(tab_5, text="poisson", command=open_decision_tree_window)
poisson_button.pack(padx=10, pady=10)

tweedie_button = customtkinter.CTkButton(tab_5, text="tweedie", command=open_decision_tree_window)
tweedie_button.pack(padx=10, pady=10)

# Lars / Lasso based models
lars_cv_button = customtkinter.CTkButton(tab_5, text="lars", command=open_decision_tree_window)
lars_cv_button.pack(padx=10, pady=10)

lasso_cv_button = customtkinter.CTkButton(tab_5, text="lasso", command=open_decision_tree_window)
lasso_cv_button.pack(padx=10, pady=10)

lasso_lars_cv_button = customtkinter.CTkButton(tab_5, text="lasso-lars", command=open_decision_tree_window)
lasso_lars_cv_button.pack(padx=10, pady=10)

lasso_lars_ic_button = customtkinter.CTkButton(tab_5, text="lasso-lars w/ info criteria", command=open_decision_tree_window)
lasso_lars_ic_button.pack(padx=10, pady=10)

# Ridge based models
ridge_cv_button = customtkinter.CTkButton(tab_5, text="ridge", command=open_decision_tree_window)
ridge_cv_button.pack(padx=10, pady=10)

bays_ridge_button = customtkinter.CTkButton(tab_5, text="baesian ridge", command=open_decision_tree_window)
bays_ridge_button.pack(padx=10, pady=10)

# Elastic nets
enet_cv_button = customtkinter.CTkButton(tab_5, text="elastic net", command=open_decision_tree_window)
enet_cv_button.pack(padx=10, pady=10)

# Quantile
quantile_button = customtkinter.CTkButton(tab_5, text="quantile", command=open_decision_tree_window)
quantile_button.pack(padx=10, pady=10)

# Support vector based models
svr_button = customtkinter.CTkButton(tab_5, text="support vector", command=open_decision_tree_window)
svr_button.pack(padx=10, pady=10)

lin_svr_button = customtkinter.CTkButton(tab_5, text="linear svr", command=open_decision_tree_window)
lin_svr_button.pack(padx=10, pady=10)

nu_svr_button = customtkinter.CTkButton(tab_5, text="nu svr", command=open_decision_tree_window)
nu_svr_button.pack(padx=10, pady=10)

ts_svr_button = customtkinter.CTkButton(tab_5, text="time series svr", command=open_decision_tree_window)
ts_svr_button.pack(padx=10, pady=10)

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

# Put stuff in tab 7 - Historical Data
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