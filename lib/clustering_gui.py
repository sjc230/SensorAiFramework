import customtkinter
from tkinter import Toplevel, Label, Entry, Button
import customtkinter
from utils import parse_text_entry, convert_list_to_string, load_gui_data
from clustering import *


global clust_queue_names
global clust_queue_models

clust_queue_names = []
clust_queue_models = []

def add_to_clust_queue(name,model):
    global clust_queue_names
    clust_queue_names.append(name)
    clust_queue_models.append(model)
    print("Queue: ", clust_queue_names)

def show_clust_queue():
    global clust_queue_names
    clust_queue_window = customtkinter.CTkToplevel()
    clust_queue_window.title("Clustering Queue")
    clust_queue_window.geometry("200x400")
    clust_queue_window.attributes('-topmost', True)

    queue_string = convert_list_to_string(clust_queue_names)
    queue_label = customtkinter.CTkLabel(master=clust_queue_window,text=queue_string)
    queue_label.pack()

def reset_clust_queue():
    global clust_queue_names
    global clust_queue_models
    clust_queue_names = []
    clust_queue_models = []

def execute_clust_gridsearch():
    global clust_queue_names
    global clust_queue_models

    X_train, y_train, X_test, y_test = load_gui_data()

    gridsearch_clustering(names=clust_queue_names,pipes=clust_queue_models,X=X_test,y=y_test,plot_number=3,save_best=True)


# Affinity Propagation Window
def open_affin_prop_window():
    dampening = 0.5
    max_iterations = 200
    verbose = 'False'
    random_state = 'None'


    def retrieve_data():
        damp = dampening_entry.get()
        max_it = max_it_entry.get()
        verb = verbose_entry.get()
        rand_st = random_state_entry.get()

        damenping_list = parse_text_entry(damp,'float')
        max_it_list = parse_text_entry(max_it,'int')
        verbose_list = parse_text_entry(verb,'bool')
        random_state_list = parse_text_entry(rand_st,'int')

        name = "Affinity Progagation"
        aff_prop = pipeBuild_AffinityPropagation(damping=damenping_list, max_iter=max_it_list, verbose=verbose_list, random_state=random_state_list[0])
        add_to_clust_queue(name,aff_prop)
        print("Affinity Progagation Model Created")

    affin_prop_window = customtkinter.CTkToplevel()
    affin_prop_window.title("Decision Tree Pipe Builder")
    affin_prop_window.geometry("500x500")
    affin_prop_window.attributes('-topmost', True)

    dampening_label = customtkinter.CTkLabel(affin_prop_window, text="Dampening: floats")
    dampening_label.pack()

    dampening_entry = customtkinter.CTkEntry(affin_prop_window)
    dampening_entry.pack(pady=10)
    dampening_entry.insert(0, dampening)
    dampening_entry.pack(pady=10)

    max_it_label = customtkinter.CTkLabel(affin_prop_window, text="Max Iterations: None integers")
    max_it_label.pack()

    max_it_entry = customtkinter.CTkEntry(affin_prop_window)
    max_it_entry.pack(pady=10)
    max_it_entry.insert(0, max_iterations)
    max_it_entry.pack(pady=10)

    verbose_label = customtkinter.CTkLabel(affin_prop_window, text="Verbose: True, False")
    verbose_label.pack()

    verbose_entry = customtkinter.CTkEntry(affin_prop_window)
    verbose_entry.pack(pady=10)
    verbose_entry.insert(0, verbose)
    verbose_entry.pack(pady=10)

    random_label = customtkinter.CTkLabel(affin_prop_window, text="Random State: None or a single integer")
    random_label.pack()

    random_state_entry = customtkinter.CTkEntry(affin_prop_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(affin_prop_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# DBSCAN Window
def open_dbscan_window():
    eps = 0.5
    min_samples = 5
    metric = 'euclidean'
    algorithm = 'auto'
    leaf_size = 30
    p = 'None'


    def retrieve_data():
        e = eps_entry.get()
        ms = min_samp_entry.get()
        m = metric_entry.get()
        a = algo_entry.get()
        lf = leaf_entry.get()
        p = power_entry.get()

        eps_list = parse_text_entry(e,'float')
        min_samp_list = parse_text_entry(ms,'int')
        metric_list = parse_text_entry(m,'string')
        algo_list = parse_text_entry(a,'string')
        leaf_list = parse_text_entry(lf,'int')
        power_list = parse_text_entry(p,'float')

        name = "DBSCAN"
        dbscan = pipeBuild_DBSCAN(eps=eps_list, min_samples=min_samp_list, metric=metric_list, algorithm=algo_list, leaf_size=leaf_list, p=power_list)
        add_to_clust_queue(name,dbscan)
        print("DBSCAN Model Created")

    dbscan_window = customtkinter.CTkToplevel()
    dbscan_window.title("DBSCAN Pipe Builder")
    dbscan_window.geometry("500x550")
    dbscan_window.attributes('-topmost', True)

    eps_label = customtkinter.CTkLabel(dbscan_window, text="Eps: floats")
    eps_label.pack()

    eps_entry = customtkinter.CTkEntry(dbscan_window)
    eps_entry.pack(pady=10)
    eps_entry.insert(0, eps)
    eps_entry.pack(pady=10)

    min_samp_label = customtkinter.CTkLabel(dbscan_window, text="Minimum Samples: integers")
    min_samp_label.pack()

    min_samp_entry = customtkinter.CTkEntry(dbscan_window)
    min_samp_entry.pack(pady=10)
    min_samp_entry.insert(0, min_samples)
    min_samp_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(dbscan_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(dbscan_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)      

    algo_label = customtkinter.CTkLabel(dbscan_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(dbscan_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)

    leaf_label = customtkinter.CTkLabel(dbscan_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(dbscan_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    power_label = customtkinter.CTkLabel(dbscan_window, text="Power: floats only")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(dbscan_window)
    power_entry.pack(pady=10)
    power_entry.insert(0, p)
    power_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(dbscan_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# OPTICS Window
def open_optics_window():
    cluster_method = 'xi'
    xi = 0.05
    eps = 0.5
    min_samples = 5
    metric = 'euclidean'
    algorithm = 'auto'
    leaf_size = 30
    p = 'None'


    def retrieve_data():
        cm = method_entry.get()
        x = xi_entry.get()
        e = eps_entry.get()
        ms = min_samp_entry.get()
        m = metric_entry.get()
        a = algo_entry.get()
        lf = leaf_entry.get()
        p = power_entry.get()

        method_list = parse_text_entry(cm,'string')
        xi_list = parse_text_entry(x,'float')
        eps_list = parse_text_entry(e,'float')
        min_samp_list = parse_text_entry(ms,'int')
        metric_list = parse_text_entry(m,'string')
        algo_list = parse_text_entry(a,'string')
        leaf_list = parse_text_entry(lf,'int')
        power_list = parse_text_entry(p,'float')

        name = "OPTICS"
        optics = pipeBuild_OPTICS(cluster_method=method_list,xi=xi_list,eps=eps_list, min_samples=min_samp_list, metric=metric_list, algorithm=algo_list, leaf_size=leaf_list, p=power_list)
        add_to_clust_queue(name,optics)
        print("OPTICS Model Created")

    optics_window = customtkinter.CTkToplevel()
    optics_window.title("OPTICSN Pipe Builder")
    optics_window.geometry("500x650")
    optics_window.attributes('-topmost', True)

    method_label = customtkinter.CTkLabel(optics_window, text="Cluster Method: dbscan, xi")
    method_label.pack()

    method_entry = customtkinter.CTkEntry(optics_window)
    method_entry.pack(pady=10)
    method_entry.insert(0, cluster_method)
    method_entry.pack(pady=10)

    xi_label = customtkinter.CTkLabel(optics_window, text="Xi: floats between 0 and 1")
    xi_label.pack()

    xi_entry = customtkinter.CTkEntry(optics_window)
    xi_entry.pack(pady=10)
    xi_entry.insert(0, xi)
    xi_entry.pack(pady=10)

    eps_label = customtkinter.CTkLabel(optics_window, text="Eps: floats")
    eps_label.pack()

    eps_entry = customtkinter.CTkEntry(optics_window)
    eps_entry.pack(pady=10)
    eps_entry.insert(0, eps)
    eps_entry.pack(pady=10)

    min_samp_label = customtkinter.CTkLabel(optics_window, text="Minimum Samples: integers")
    min_samp_label.pack()

    min_samp_entry = customtkinter.CTkEntry(optics_window)
    min_samp_entry.pack(pady=10)
    min_samp_entry.insert(0, min_samples)
    min_samp_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(optics_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(optics_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)      

    algo_label = customtkinter.CTkLabel(optics_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(optics_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)

    leaf_label = customtkinter.CTkLabel(optics_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(optics_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    power_label = customtkinter.CTkLabel(optics_window, text="Power: floats only")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(optics_window)
    power_entry.pack(pady=10)
    power_entry.insert(0, p)
    power_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(optics_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)

# Mean Shift Window
def open_mean_shift_window():
    bandwidth = 'None'
    bin_seeding = 'True'
    min_bin_freq = 1
    cluster_all = 'True'
    max_iter = 300

    def retrieve_data():
        b = bandwidth_entry.get()
        bs = bin_seeding_entry.get()
        mbf = min_bin_freq_entry.get()
        ca = cluster_all_entry.get()
        mi = max_iter_entry.get()

        bandwidth_list = parse_text_entry(b,'float')
        bin_list = parse_text_entry(bs,'bool')
        min_freq_list = parse_text_entry(mbf,'int')
        cluster_list = parse_text_entry(ca,'bool')
        max_iter_list = parse_text_entry(mi,'int')
        
        name = "Mean Shift"
        optics = pipeBuild_MeanShift(bandwidth=bandwidth_list, bin_seeding=bin_list, min_bin_freq=min_freq_list, cluster_all=cluster_list, max_iter=max_iter_list)
        add_to_clust_queue(name,optics)
        print("Mean Shift Model Created")

    mean_shift_window = customtkinter.CTkToplevel()
    mean_shift_window.title("Mean Shift Pipe Builder")
    mean_shift_window.geometry("500x650")
    mean_shift_window.attributes('-topmost', True)

    bandwidth_label = customtkinter.CTkLabel(mean_shift_window, text="Bandwidth: None or floats")
    bandwidth_label.pack()

    bandwidth_entry = customtkinter.CTkEntry(mean_shift_window)
    bandwidth_entry.pack(pady=10)
    bandwidth_entry.insert(0, bandwidth)
    bandwidth_entry.pack(pady=10)

    bin_seeding_label = customtkinter.CTkLabel(mean_shift_window, text="Bin Seeding: True, False")
    bin_seeding_label.pack()

    bin_seeding_entry = customtkinter.CTkEntry(mean_shift_window)
    bin_seeding_entry.pack(pady=10)
    bin_seeding_entry.insert(0, bin_seeding)
    bin_seeding_entry.pack(pady=10)

    min_bin_freq_label = customtkinter.CTkLabel(mean_shift_window, text="Minimum Bin Frequency: integers")
    min_bin_freq_label.pack()

    min_bin_freq_entry = customtkinter.CTkEntry(mean_shift_window)
    min_bin_freq_entry.pack(pady=10)
    min_bin_freq_entry.insert(0, min_bin_freq)
    min_bin_freq_entry.pack(pady=10)

    cluster_all_label = customtkinter.CTkLabel(mean_shift_window, text="Cluster All: True, False")
    cluster_all_label.pack()

    cluster_all_entry = customtkinter.CTkEntry(mean_shift_window)
    cluster_all_entry.pack(pady=10)
    cluster_all_entry.insert(0, cluster_all)
    cluster_all_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(mean_shift_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(mean_shift_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(mean_shift_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)
