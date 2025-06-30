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
from regression import *

def add_to_regress_queue(name,model):
    st.session_state['regress_name_queue'].append(name)
    st.session_state['regress_model_queue'].append(model)
    print("Queue: ", st.session_state['regress_name_queue'])

def execute_regress_gridsearch():
    X_train = st.session_state['X_train']
    y_train = st.session_state['y_train']
    X_test = st.session_state['X_test']
    y_test = st.session_state['y_test']

    gridsearch_regressor(names=st.session_state['regress_name_queue'],pipes=st.session_state['regress_model_queue'],
                              X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,
                              scoring="neg_mean_squared_error",save_best=True,log=True)

st.title("Regression")

regress_model_tuple = ('linear', 'gamma', 'poisson', 'tweedie',
               'lars', 'lasso', 'lasso-lars', 'lasso-lars ic',
               'ridge', 'bayesian ridge', 'elastic net', 'quantile',
               'support vector', 'linear svr', 'nu svr', 'time series svr')

regress_model_box = st.selectbox('**Select the model(s) you like to use.**', regress_model_tuple)

########################################################
# Model Variable Entries
########################################################

# Linear Regression
if regress_model_box == 'linear':
    lin_fi = st.text_input("Fit Intercept: True, False", value='True', key="linear_fit_intercept")


if regress_model_box == 'linear':
    if st.button("Add Linear to Regression Queue"):    
        lin_fit_list = parse_text_entry(lin_fi,'bool')

        name = "Linear"
        linear = pipeBuild_LinearRegression(fit_intercept=lin_fit_list)
        add_to_regress_queue(name,linear)


# Gamma Regression
if regress_model_box == 'gamma':
    gam_a = st.text_input("Alpha: positive integers", value='1', key="gamma_alpha")
    gam_fi = st.text_input("Fit Intercept: True, False", value='True', key="gamma_fit_intercept")
    gam_s = st.text_input("Solver: lbfgs, newton-cholesky", value='lbfgs', key="gamma_solver")
    gam_mi = st.text_input("Max Iterations: integers", value='100', key="gamma_max_iter")
    gam_t = st.text_input("Tolerance: floats only", value='0.0001', key="gamma_fit_tol")


if regress_model_box == 'gamma':
    if st.button("Add Gamma to Regression Queue"):    
        gam_alpha_list = parse_text_entry(gam_a,'int')
        gam_fit_list = parse_text_entry(gam_fi,'bool')
        gam_solver_list = parse_text_entry(gam_s,'string')
        gam_max_iter_list = parse_text_entry(gam_mi,'int')
        gam_tol_list = parse_text_entry(gam_t,'float')

        name = "Gamma"
        gamma = pipeBuild_GammaRegressor(alpha=gam_alpha_list, fit_intercept=gam_fit_list, 
                                         solver=gam_solver_list, max_iter=gam_max_iter_list, tol=gam_tol_list)
        add_to_regress_queue(name,gamma)

########################################################
# End Model Variable Entries
########################################################

if st.button("Show Regression Model Queue"):
    print(st.session_state['regress_name_queue'])
    st.write(str(st.session_state['regress_name_queue']))

if st.button("Clear Regression Model Queue"):
    st.session_state['regress_name_queue'] = []
    st.session_state['regress_model_queue'] = []
    st.session_state["regress log loader"] = None
    st.session_state['show_regress_log'] = False

if st.button("Run Regression Grid Search"):
    print("Regression gridsearch started")
    st.session_state['show_regress_log'] = True
    execute_regress_gridsearch()

if st.session_state['show_regress_log'] == True:
    log_file = st.file_uploader("Choose a txt file", type="txt",key="regress log loader")
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