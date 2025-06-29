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
from utils import parse_text_entry
from clustering import *

def add_to_clust_queue(name,model):
    st.session_state['clust_name_queue'].append(name)
    st.session_state['clust_model_queue'].append(model)
    print("Queue: ", st.session_state['clust_name_queue'])

def execute_clust_gridsearch():
    X_train = st.session_state['X_train']
    y_train = st.session_state['y_train']
    X_test = st.session_state['X_test']
    y_test = st.session_state['y_test']

    gridsearch_clustering(names=st.session_state['clust_name_queue'],pipes=st.session_state['clust_model_queue'],
                          X=X_test,y=y_test,plot_number=3,save_best=True,log=True)

st.title("Clustering")

clust_model_tuple = ('affinity propagation', 'dbscan', 'optics', 'k means',
               'bisecting k means', 'mini-batch k means', 'time series k means',
               'spectral clustering')

clust_model_box = st.selectbox('**Select the model(s) you like to use.**', clust_model_tuple)

########################################################
# Model Variable Entries
########################################################

# Affinity Propagation
if clust_model_box == 'affinity propagation':
    ap_damp = st.text_input("Dampening: floats", value='0.5', key="aff_prop_dampening")
    ap_max_it = st.text_input("Max Iterations: None or integers", value='200', key="aff_prop_max_iterations")
    ap_verb = st.text_input("Verbose: True, False", value='False', key="aff_prop_verbose")
    ap_rand = st.text_input("Random State: None or a single integer", value='None', key="aff_prop_random_state")


if clust_model_box == 'affinity propagation':
    if st.button("Add Affinity Propagation to Clustering Queue"):    
        ap_dampening_list = parse_text_entry(ap_damp,'float')
        ap_max_iter_list = parse_text_entry(ap_max_it,'int')
        ap_verbose_list = parse_text_entry(ap_verb,'bool')
        ap_random_state_list = parse_text_entry(ap_rand,'int')
        name = "Affinity Propagation"
        aff_prop = pipeBuild_AffinityPropagation(damping=ap_dampening_list, max_iter=ap_max_iter_list, 
                                                 verbose=ap_verbose_list, random_state=ap_random_state_list[0])
        add_to_clust_queue(name,aff_prop)

# DBSCAN
if clust_model_box == 'dbscan':
    dbscan_eps = st.text_input("Eps: floats", value='0.5', key="dbscan_eps")
    dbscan_min_samp = st.text_input("Minimum Samples: integers", value='5', key="dbscan_min_samples")
    dbscan_metric = st.text_input("Distance Metric: euclidean, manhattan, chebyshev, minkowski", value='euclidean', key="dbscan_metric")
    dbscan_algo = st.text_input("Algorithm: auto, ball_tree, kd_tree, brute", value='auto', key="dbscan_algorithm")
    dbscan_ls = st.text_input("Leaf Size: integers", value='30', key="dbscan_leaf_size")
    dbscan_p = st.text_input("Power: floats", value='None', key="dbscan_p")


if clust_model_box == 'dbscan':
    if st.button("Add DBSCAN to Clustering Queue"):    
        dbscan_eps_list = parse_text_entry(dbscan_eps,'float')
        dbscan_min_samp_list = parse_text_entry(dbscan_min_samp,'int')
        dbscan_metric_list = parse_text_entry(dbscan_metric,'string')
        dbscan_algo_list = parse_text_entry(dbscan_algo,'string')
        dbscan_ls_list = parse_text_entry(dbscan_ls,'int')
        dbscan_p_list = parse_text_entry(dbscan_p,'float')
        
        name = "DBSCAN"
        dbscan = pipeBuild_DBSCAN(eps=dbscan_eps_list, min_samples=dbscan_min_samp_list, metric=dbscan_metric_list, 
                                           algorithm=dbscan_algo_list, leaf_size=dbscan_ls_list, p=dbscan_p_list)
        add_to_clust_queue(name,dbscan)

# OPTICS
if clust_model_box == 'optics':
    optics_method = st.text_input("Cluster Method: dbscan, xi", value='xi', key="optics_method")
    optics_xi = st.text_input("Xi: floats between 0 and 1", value='0.05', key="optics_xi")
    optics_eps = st.text_input("Eps: floats", value='0.5', key="optics_eps")
    optics_min_samp = st.text_input("Minimum Samples: integers", value='5', key="optics_min_samples")
    optics_metric = st.text_input("Distance Metric: euclidean, manhattan, chebyshev, minkowski", value='euclidean', key="optics_metric")
    optics_algo = st.text_input("Algorithm: auto, ball_tree, kd_tree, brute", value='auto', key="optics_algorithm")
    optics_ls = st.text_input("Leaf Size: integers", value='30', key="optics_leaf_size")
    optics_p = st.text_input("Minkowski Parameter: 1 or 2 only", value='2', key="optics_p")


if clust_model_box == 'optics':
    if st.button("Add OPTICS to Clustering Queue"):
        optics_method_list = parse_text_entry(optics_method,'string')
        optics_xi_list = parse_text_entry(optics_xi,'float')    
        optics_eps_list = parse_text_entry(optics_eps,'float')
        optics_min_samp_list = parse_text_entry(optics_min_samp,'int')
        optics_metric_list = parse_text_entry(optics_metric,'string')
        optics_algo_list = parse_text_entry(optics_algo,'string')
        optics_ls_list = parse_text_entry(optics_ls,'int')
        optics_p_list = parse_text_entry(optics_p,'float')
        
        name = "OPTICS"
        optics = pipeBuild_OPTICS(cluster_method=optics_method_list, xi=optics_xi_list, eps=optics_eps_list, 
                                  min_samples=optics_min_samp_list, metric=optics_metric_list, 
                                  algorithm=optics_algo_list, leaf_size=optics_ls_list, p=optics_p_list)
        add_to_clust_queue(name,optics)

########################################################
# End Model Variable Entries
########################################################

if st.button("Show Clustering Model Queue"):
    print(st.session_state['clust_name_queue'])
    st.write(str(st.session_state['clust_name_queue']))

if st.button("Clear Clustering Model Queue"):
    st.session_state['clust_name_queue'] = []
    st.session_state['clust_model_queue'] = []
    st.session_state["clust log loader"] = None
    st.session_state['show_clust_log'] = False

if st.button("Run Clustering Grid Search"):
    print("Clustering gridsearch started")
    st.session_state['show_clust_log'] = True
    execute_clust_gridsearch()

if st.session_state['show_clust_log'] == True:
    log_file = st.file_uploader("Choose a txt file", type="txt",key="clust log loader")
    if log_file is not None:
        root, extension = os.path.splitext(log_file.name)
        if extension.lower() == ".txt":
            bytes_data = log_file.getvalue()  
            string_data = bytes_data.decode('utf-8') 
            # Display the content
            st.write("File Content:")
            st.code(string_data, language="text") # Use st.code for displaying raw text            
        else:
            st.write("You have selected an incorrect file type")