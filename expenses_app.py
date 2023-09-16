# %%
import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import re
from math import ceil
from myfuncs import plot_func, plot_func_st, check_password

plt.gcf().autofmt_xdate() # not sure if this makes any difference for the x axis



# %%






if check_password():


    # Function to preprocess the data
    def preprocess_data(df):
        # Drop rows with missing values
        df.dropna(inplace=True)
        
        # Keep the specified columns
        columns_to_keep = [
            'Category',
            'Transaction Details',
            'Transaction Date',
            'Transaction Comments / Reference Code',
            'Amount'
        ]
        df = df[columns_to_keep]
        
        # Rename columns
        df.rename(columns={'Transaction Comments / Reference Code': 'Transaction'}, inplace=True)
        
        # Convert column names to snake case
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Convert the 'transaction_date' column to datetime format
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%d/%m/%Y')
        
        # Remove records where the amount is larger than 0
        df = df[df['amount'] <= 0]

        return df

    # Streamlit app
    st.title("Home Money Tracker App 🏠💰📊")

    uploaded_file = st.file_uploader("Upload an excel file with financial transactions", type="xlsx")

    if uploaded_file:
        data = pd.read_excel(uploaded_file, engine='openpyxl')
        data = preprocess_data(data)
        
        # Date Range Selector
            # Date Range Selector
        start_date, end_date = st.date_input("Select date range", [data['transaction_date'].min().date(), data['transaction_date'].max().date()])
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        data = data[(data['transaction_date'] >= start_date) & (data['transaction_date'] <= end_date)]

        
        # Category Selector
        categories = st.multiselect("Select categories", data['category'].unique())
        if categories:
            data = data[data['category'].isin(categories)]
        
        # Transaction Search
        search_string = st.text_input("Search for a string in transactions (supports regex)")
        if search_string:
            data = data[data['transaction'].apply(lambda x: bool(re.search(search_string, x)))]
        
        # Bar graph showing total amount by month
        data['month_year'] = data['transaction_date'].dt.to_period('M')
        monthly_data = data.groupby('month_year')['amount'].sum().reset_index()
        monthly_data['amount'] = -monthly_data['amount']
        monthly_data['month_year'] = monthly_data['month_year'].astype(str)
        st.bar_chart(monthly_data.set_index('month_year'))

        # Display the selected categories
        if categories:
            st.write(f"Selected Categories: {', '.join(categories)}")
        else:
            st.write("All Categories are selected.")
        
        # Display data in tabular format
        st.dataframe(data)






#CODE HERE

 
 
 
 
 

hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # %%
