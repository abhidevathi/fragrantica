import streamlit as st
import pandas as pd
import numpy as np

st.write("Hello World")

cols = 3
rows = 20
dataframe = pd.DataFrame(
    np.random.randn(rows, cols), # create a random dataframe with 5 columns and 20 rows with values between 0 and 1
    columns=('col %d' % i for i in range(cols)))

st.dataframe(dataframe.style.highlight_max(axis=0)) # Dataframe with highlights

# st.table(dataframe) # Static Table

st.header("Line Chart", divider='blue')

chart_data = pd.DataFrame(
     np.random.randn(rows, cols),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)


st.header("Map", divider='blue')
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

st.header("Widget", divider="blue")

x = st.slider('x')
st.write(x, 'squared is', x * x)