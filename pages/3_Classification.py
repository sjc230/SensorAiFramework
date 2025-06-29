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
from classification import *

def add_to_class_queue(name,model):
    st.session_state['class_name_queue'].append(name)
    st.session_state['class_model_queue'].append(model)
    print("Queue: ", st.session_state['class_name_queue'])

def execute_class_gridsearch():
    X_train = st.session_state['X_train']
    y_train = st.session_state['y_train']
    X_test = st.session_state['X_test']
    y_test = st.session_state['y_test']

    gridsearch_classifier(names=st.session_state['class_name_queue'],pipes=st.session_state['class_model_queue'],
                              X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,
                              plot_number=3,scoring="neg_mean_squared_error",save_best=True,log=True)
    


st.title("Classification")

model_tuple = ('decision tree', 'extra trees', 'random forest', 'gradien boosting',
               'k nearest neighbors', 'nearest centroid', 'radius nearest neighbors',
               'support vector', 'nu support vector', 'time series svc')

model_box = st.selectbox('**Select the model(s) you like to use.**', model_tuple)

########################################################
# Model Variable Entries
########################################################

# Decision Tree
if model_box == 'decision tree':
    dec_crit = st.text_input("Criterion: gini, entropy, or log_loss", value='gini', key="dec crit")
    dec_split = st.text_input("Splitter: best, random", value='best', key="dec split")
    dec_max_d = st.text_input("Maximum Tree Depth: integers", value='None', key="dec max depth")
    dec_rand = st.text_input("Random State: None or a single integer", value='None', key="dec random state")

if model_box == 'decision tree':
    if st.button("Add Decision Tree to Classifier Queue"):    
        criterion_list = parse_text_entry(dec_crit,'string')
        splitter_list = parse_text_entry(dec_split,'string')
        max_depth_list = parse_text_entry(dec_max_d,'int')
        random_state_list = parse_text_entry(dec_rand,'int')
        name = "Decision Tree"
        decision_tree = pipeBuild_DecisionTreeClassifier(criterion=criterion_list,splitter=splitter_list,max_depth=max_depth_list,random_state=random_state_list[0])
        add_to_class_queue(name,decision_tree)


# Extra Trees
if model_box == 'extra trees':
    extra_ne = st.text_input("Number of Estimators: integers", value='100', key="extra_n_estimators")
    extra_crit = st.text_input("Criterion: gini, entropy, or log_loss", value='gini', key="extra_criterion")
    extra_max_d = st.text_input("Maximum Tree Depth: integers", value='None', key="extra_max_depth")
    extra_rand = st.text_input("Random State: None or a single integer", value='None', key="extra_random_state")
    extra_ms_split = st.text_input("Minimum Sample # for Node Splits: integers", value='2', key="extra_min_samples_split")
    extra_ms_leaf = st.text_input("Minimum Sample # Required for a Leaf: integers", value='1', key="extra_min_samples_leaf")

if model_box == 'extra trees':
    if st.button("Add Extra Trees to Classifier Queue"): 
        extra_ne_list = parse_text_entry(extra_ne,'int')   
        extra_crit_list = parse_text_entry(extra_crit,'string')
        extra_max_d_list = parse_text_entry(extra_max_d,'int')
        extra_rand_list = parse_text_entry(extra_rand,'int')
        extra_ms_split_list = parse_text_entry(extra_ms_split,'int')
        extra_ms_leaf_list = parse_text_entry(extra_ms_leaf,'int')
        name = "Extra Trees"
        extra_trees = pipeBuild_ExtraTreesClassifier(n_estimators=extra_ne_list,criterion=extra_crit_list,max_depth=extra_max_d_list,min_samples_split=extra_ms_split_list,min_samples_leaf=extra_ms_leaf_list,random_state=extra_rand_list[0])
        add_to_class_queue(name,extra_trees)

# Random Forest
if model_box == 'random forest':
    rfor_ne = st.text_input("Number of Estimators: integers", value='100', key="forest_n_estimators")
    rfor_crit = st.text_input("Criterion: gini, entropy, or log_loss", value='gini', key="forest_criterion")
    rfor_max_d = st.text_input("Maximum Tree Depth: integers", value='None', key="forest_max_depth")
    rfor_rand = st.text_input("Random State: None or a single integer", value='None', key="forest_random_state")

if model_box == 'random forest':
    if st.button("Add Random Forest to Classifier Queue"):
        rfor_ne_list = parse_text_entry(rfor_ne,'int')    
        rfor_crit_list = parse_text_entry(rfor_crit,'string')
        rfor_max_d_list = parse_text_entry(rfor_max_d,'int')
        rfor_rand_list = parse_text_entry(rfor_rand,'int')
        name = "Random Forest"
        random_forest = pipeBuild_RandomForestClassifier(n_estimators=rfor_ne_list,criterion=rfor_crit_list,max_depth=rfor_max_d_list,random_state=rfor_rand_list[0])
        add_to_class_queue(name,random_forest)

########################################################
# End Model Variable Entries
########################################################

if st.button("Show Classifier Model Queue"):
    print(st.session_state['class_name_queue'])
    st.write(str(st.session_state['class_name_queue']))

if st.button("Clear Classifier Model Queue"):
    st.session_state['class_name_queue'] = []
    st.session_state['class_model_queue'] = []
    st.session_state["class log loader"] = None
    st.session_state['show_class_log'] = False

if st.button("Run Classifier Grid Search"):
    print("Classifier gridsearch started")
    st.session_state['show_class_log'] = True
    execute_class_gridsearch()

if st.session_state['show_class_log'] == True:
    log_file = st.file_uploader("Choose a txt file", type="txt",key="class log loader")
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
