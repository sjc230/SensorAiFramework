import customtkinter
from tkinter import Toplevel, Label, Entry, Button
import customtkinter
from utils import parse_text_entry, convert_list_to_string, load_gui_data
from detection import *


global detect_queue_names
global detect_queue_models
global outlier_queue_names
global outlier_queue_models

detect_queue_names = []
detect_queue_models = []
outlier_queue_names = []
outlier_queue_models = []

def add_to_detect_queue(name,model,nov=False):
    global detect_queue_names
    global outlier_queue_names

    if nov == True:
        detect_queue_names.append(name)
        detect_queue_models.append(model)
        print("Queue: ", detect_queue_names)
    else:
        outlier_queue_names.append(name)
        outlier_queue_models.append(model)
        print("Queue: ", outlier_queue_names)

def show_detect_queue(nov=False):
    global detect_queue_names
    global outlier_queue_names

    if nov == True:
        detect_queue_window = customtkinter.CTkToplevel()
        detect_queue_window.title("Novelty Detection Queue")
        detect_queue_window.geometry("200x400")
        detect_queue_window.attributes('-topmost', True)

        queue_string = convert_list_to_string(detect_queue_names)
        queue_label = customtkinter.CTkLabel(master=detect_queue_window,text=queue_string)
        queue_label.pack()
    else:
        outlier_queue_window = customtkinter.CTkToplevel()
        outlier_queue_window.title("Outlier Detection Queue")
        outlier_queue_window.geometry("200x400")
        outlier_queue_window.attributes('-topmost', True)

        queue_string = convert_list_to_string(outlier_queue_names)
        queue_label = customtkinter.CTkLabel(master=outlier_queue_window,text=queue_string)
        queue_label.pack()
       

def reset_detect_queue(nov=False):
    global detect_queue_names
    global detect_queue_models
    global outlier_queue_names
    global outlier_queue_models
    
    if nov == True:
        detect_queue_names = []
        detect_queue_models = []
    else:
        outlier_queue_names = []
        outlier_queue_models = []
    

def execute_detect_gridsearch(nov=False):
    global detect_queue_names
    global detect_queue_models
    global outlier_queue_names
    global outlier_queue_models

    X_train, y_train, X_test, y_test = load_gui_data()

    if nov == True:
        gridsearch_outlier(names=detect_queue_names,pipes=detect_queue_models,
                              X=X_test,y=y_test,
                              plot_number=3,save_best=True)
    else:
        gridsearch_outlier(names=outlier_queue_names,pipes=outlier_queue_models,
                              X=X_test,y=y_test,
                              plot_number=3,save_best=True)



# Local Outlier Factor Novelty Detection
def open_lof_nov_window():
    n_neighbors = 20
    algorithm = 'auto'
    leaf_size = 30
    metric = 'minkowski'    
    p = 2    

    def retrieve_data():
        nn = nn_entry.get()
        algo = algo_entry.get()
        leaf = leaf_entry.get()
        power = power_entry.get()
        met = metric_entry.get()
        
        nn_list = parse_text_entry(nn,'int')
        algo_list = parse_text_entry(algo,'string')
        leaf_list = parse_text_entry(leaf,'int')
        power_list = parse_text_entry(power,'int')
        metric_list = parse_text_entry(met,'string')
        

        name = "LOT Novelty Detection"
        lotn = pipeBuild_LocalOutlierFactor(n_neighbors=nn_list,algorithm=algo_list,leaf_size=leaf_list,p=power_list,metric=metric_list,novelty=[True])
        add_to_detect_queue(name,lotn,nov=True)
        print("Lot Novelty Detection Model Created")

    lotn_window = customtkinter.CTkToplevel()
    lotn_window.title("LOT Novelty Detection Pipe Builder")
    lotn_window.geometry("500x550")
    lotn_window.attributes('-topmost', True)

    nn_label = customtkinter.CTkLabel(lotn_window, text="Number of Neighbors: integers only")
    nn_label.pack()

    nn_entry = customtkinter.CTkEntry(lotn_window)
    nn_entry.pack(pady=10)
    nn_entry.insert(0, n_neighbors)
    nn_entry.pack(pady=10)

    algo_label = customtkinter.CTkLabel(lotn_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(lotn_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)     

    leaf_label = customtkinter.CTkLabel(lotn_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(lotn_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    power_label = customtkinter.CTkLabel(lotn_window, text="Power: intergers only")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(lotn_window)
    power_entry.pack(pady=10)
    power_entry.insert(0, p)
    power_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(lotn_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(lotn_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(lotn_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)
    

# Local Outlier Factor - Outlier Detection
def open_lof_out_window():
    n_neighbors = 20
    algorithm = 'auto'
    leaf_size = 30
    metric = 'minkowski'    
    p = 2    

    def retrieve_data():
        nn = nn_entry.get()
        algo = algo_entry.get()
        leaf = leaf_entry.get()
        power = power_entry.get()
        met = metric_entry.get()
        
        nn_list = parse_text_entry(nn,'int')
        algo_list = parse_text_entry(algo,'string')
        leaf_list = parse_text_entry(leaf,'int')
        power_list = parse_text_entry(power,'int')
        metric_list = parse_text_entry(met,'string')
        

        name = "LOT Outlier Detection"
        lot = pipeBuild_LocalOutlierFactor(n_neighbors=nn_list,algorithm=algo_list,leaf_size=leaf_list,p=power_list,metric=metric_list,novelty=[False])
        add_to_detect_queue(name,lot)
        print("Lot Outlier Detection Model Created")

    lot_window = customtkinter.CTkToplevel()
    lot_window.title("LOT Outlier Detection Pipe Builder")
    lot_window.geometry("500x550")
    lot_window.attributes('-topmost', True)

    nn_label = customtkinter.CTkLabel(lot_window, text="Number of Neighbors: integers only")
    nn_label.pack()

    nn_entry = customtkinter.CTkEntry(lot_window)
    nn_entry.pack(pady=10)
    nn_entry.insert(0, n_neighbors)
    nn_entry.pack(pady=10)

    algo_label = customtkinter.CTkLabel(lot_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(lot_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)     

    leaf_label = customtkinter.CTkLabel(lot_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(lot_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    power_label = customtkinter.CTkLabel(lot_window, text="Power: intergers only")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(lot_window)
    power_entry.pack(pady=10)
    power_entry.insert(0, p)
    power_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(lot_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(lot_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(lot_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)

# Local Outlier Factor - Outlier Detection
def open_lof_out_window():
    n_neighbors = 20
    algorithm = 'auto'
    leaf_size = 30
    metric = 'minkowski'    
    p = 2    

    def retrieve_data():
        nn = nn_entry.get()
        algo = algo_entry.get()
        leaf = leaf_entry.get()
        power = power_entry.get()
        met = metric_entry.get()
        
        nn_list = parse_text_entry(nn,'int')
        algo_list = parse_text_entry(algo,'string')
        leaf_list = parse_text_entry(leaf,'int')
        power_list = parse_text_entry(power,'int')
        metric_list = parse_text_entry(met,'string')
        

        name = "LOT Outlier Detection"
        lot = pipeBuild_LocalOutlierFactor(n_neighbors=nn_list,algorithm=algo_list,leaf_size=leaf_list,p=power_list,metric=metric_list,novelty=[False])
        add_to_detect_queue(name,lot)
        print("Lot Outlier Detection Model Created")

    lot_window = customtkinter.CTkToplevel()
    lot_window.title("LOT Outlier Detection Pipe Builder")
    lot_window.geometry("500x550")
    lot_window.attributes('-topmost', True)

    nn_label = customtkinter.CTkLabel(lot_window, text="Number of Neighbors: integers only")
    nn_label.pack()

    nn_entry = customtkinter.CTkEntry(lot_window)
    nn_entry.pack(pady=10)
    nn_entry.insert(0, n_neighbors)
    nn_entry.pack(pady=10)

    algo_label = customtkinter.CTkLabel(lot_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(lot_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)     

    leaf_label = customtkinter.CTkLabel(lot_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(lot_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    power_label = customtkinter.CTkLabel(lot_window, text="Power: intergers only")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(lot_window)
    power_entry.pack(pady=10)
    power_entry.insert(0, p)
    power_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(lot_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(lot_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(lot_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)