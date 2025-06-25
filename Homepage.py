import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sensor AI Framework",
)

st.title("Sensor AI Framework")
st.write("Welcome to the Center for Cyber-Physical Systems' artificial intelligence framework for sensor data")
st.sidebar.success("Select a page above")

if "X_train" not in st.session_state:
    st.session_state["X_train"] = ""

if "y_train" not in st.session_state:
    st.session_state["y_train"] = ""

if "X_test" not in st.session_state:
    st.session_state["X_test"] = ""

if "y_test" not in st.session_state:
    st.session_state["y_test"] = ""

if st.session_state.get("X_train") != None:
    st.write("X_train is loaded")

if st.session_state.get("y_train") != None:
    st.write("y_train is loaded")

if st.session_state.get("X_test") != None:
    st.write("X_test is loaded")

if st.session_state.get("y_test") != None:
    st.write("y_test is loaded")