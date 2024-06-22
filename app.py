import streamlit as st
import pandas as pd

file = st.file_uploader('Upload csv')

if file is not None:
    df = pd.read_excel(file)
    st.dataframe(df)