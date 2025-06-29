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

clust_model_tuple = ('decision tree', 'extra trees', 'random forest', 'gradien boosting',
               'k nearest neighbors', 'nearest centroid', 'radius nearest neighbors',
               'support vector', 'nu support vector', 'time series svc')

clust_model_box = st.selectbox('**Select the model(s) you like to use.**', clust_model_tuple)

if clust_model_box == 'decision tree':
    dec_crit = st.text_input("Criterion: gini, entropy, or log_los", value='gini', key="dec crit")
    dec_split = st.text_input("Splitter: best, random", value='best', key="dec split")
    dec_max_d = st.text_input("Maximum Tree Depth: integers", value='None', key="dec max depth")
    dec_rand = st.text_input("Random State: None or a single integer", value='None', key="dec random state")



if st.button("Add Model to Clustering Queue"):
    if clust_model_box == 'decision tree':
        criterion_list = parse_text_entry(dec_crit,'string')
        splitter_list = parse_text_entry(dec_split,'string')
        max_depth_list = parse_text_entry(dec_max_d,'int')
        random_state_list = parse_text_entry(dec_rand,'int')
        name = "Decision Tree"
        decision_tree = pipeBuild_DecisionTreeClassifier(criterion=criterion_list,splitter=splitter_list,max_depth=max_depth_list,random_state=random_state_list[0])
        add_to_clust_queue(name,decision_tree)


if st.button("Show Clustering Model Queue"):
    print(st.session_state['clust_name_queue'])

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