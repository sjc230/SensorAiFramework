import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose an NPY file", type="npy")

if uploaded_file is not None:
    data = np.load(uploaded_file)
    st.write("File uploaded ...")

    st.subheader("Data Preview")
    df = pd.DataFrame(data)
    st.write(df.head())

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select Column to filter by",columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select the x-axis column", columns)
    y_column = st.selectbox("Select the y-axis column", columns)

    if st.button("Generate Plot"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])
    
else:
    st.write("Waiting on file upload")