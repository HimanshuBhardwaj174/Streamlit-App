import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('data.csv')
st.set_page_config(layout='wide',page_title='Finance Analysis')
with st.sidebar:
    st.title('Analysis')
    box = st.selectbox('Type',['Overall','Startup','Investor'])

if box == 'Overall':
    def over():
        total,max,mean = round(df['Amount in Cr'].sum()),round(df['Amount in Cr'].max()),round(df['Amount in Cr'].mean())
        col1,col2,col3 = st.columns(3)
        col1.metric('Total Overall Investment',str(total) + 'Cr')
        col2.metric('Max Investment',str(max) + 'Cr')
        col3.metric('Average Investment',str(mean) + 'Cr')
        total_startup = df['Startup Name'].nunique()
        st.metric('Total Funded Startup',total_startup)
    st.title('Overall Analysis')
    but1 = st.sidebar.button('Find Overall Analysis')
    if but1 :
        over()


elif box == 'Startup':
    name = st.sidebar.selectbox('Name',df['Startup Name'].unique())
    st.title('Startup Analysis')
    def info():
        curr_data = df[df['Startup Name']==name]
        st.subheader(f"Startup Name: {name}")
        col1, col2 ,col3= st.columns(3)
        col1.metric('Industry :',curr_data['Industry Vertical'].unique()[0])
        col2.metric('Sub Industry',curr_data['SubVertical'].values[0])
        col3.metric('Location',curr_data['City  Location'].values[0])
        
        st.subheader('Funding Round')
        st.code("""
        curr_data[['City  Location','Investors Name','Date']]
        """)
        st.dataframe(curr_data[['City  Location','Investors Name','Date']])

        st.info('Similar Company')
        st.dataframe(df[df['Startup Name'].str.lower().str.contains(name.lower())]['Startup Name'])


    but1 = st.sidebar.button('Startup Analysis')
    if but1:
        info()

























else:

    def info(name):
        curr_data = df[df['Investors Name'].str.contains(name)]
        st.header(f'Name -{name}',name)
        st.subheader('Recent 5 Investment')
        st.dataframe(curr_data.sort_values(by='Date',ascending=False).head())
        
        big_df = curr_data.groupby('Startup Name')['Amount in Cr'].sum()
        col1 ,col2 = st.columns(2)
        
        with col1:
            st.subheader('Biggest Investment')
            fig, ax = plt.subplots()
            ax.bar(big_df.sort_values(ascending=False).head().index,big_df.sort_values(ascending=False).head().values)
            st.pyplot(fig)
        with col2:
            st.subheader('Sectorwise')
            sector = curr_data.groupby('Industry Vertical')['Amount in Cr'].sum().sort_values(ascending=False).head()
            fig, ax = plt.subplots()
            ax.pie(sector,labels = sector.index,autopct='%1.1f%%')
            st.pyplot(fig) 

        col1 ,col2 = st.columns(2)
        with col1:
            st.subheader('Stage Wise')
            sector = curr_data.groupby('InvestmentnType')['Amount in Cr'].sum().sort_values(ascending=False).head()
            fig, ax =plt.subplots()
            ax.pie(sector,labels = sector.index,autopct='%1.1f%%')
            st.pyplot(fig) 
        with col2:
            st.subheader('City Wise')
            sector = curr_data.groupby('City  Location')['Amount in Cr'].sum().sort_values(ascending=False).head()
            fig, ax = plt.subplots()
            ax.pie(sector,labels = sector.index,autopct='%1.1f%%')
            st.pyplot(fig) 

        st.subheader('Year on Year Investment')
        yoy = curr_data.sort_values(by='Date')
        yoy['Year'] = pd.to_datetime(yoy['Date']).dt.year
        ser = yoy.groupby('Year')['Amount in Cr'].sum()
        fig,ax = plt.subplots(figsize=(8,8))
        ax.plot(ser.index,ser.values)
        st.pyplot(fig)


    


    invest = st.sidebar.selectbox('Name',sorted(set(df['Investors Name'].str.split(',').sum())))
    button = st.sidebar.button('Find Detail')
    if button:
        st.title('Investor Analysis')
        info(invest)
    
    