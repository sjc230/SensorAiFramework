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

if "data_file" not in st.session_state:
    st.session_state["data_file"] = ""

if "label_file" not in st.session_state:
    st.session_state["label_file"] = ""