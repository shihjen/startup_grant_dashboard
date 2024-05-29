# import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import helper

# Streamlit page configuration
st.set_page_config(page_title='Startup Grant Dashboard',
                   page_icon='📊',
                   layout='wide',
                   initial_sidebar_state='auto')

# define a custom css script
custom_css = """
<style>
.custom-title {
    background-color: #fdc590; /* Change the color code to your desired background color */
    color: #111810; /* Change the text color code to your desired color */
    padding: 12px; /* Optional: Adjust padding as needed */
}
</style>
"""

# load in the dataset
data = pd.read_csv('data/startup.csv')
processed_data = helper.process_loaded_data(data)
heatmap_data = helper.preprocess_heatmap(processed_data)

# year option for user selection to filter on dashboard
year_option = sorted(processed_data['Invoice_Year'].unique())

# sidebar
st.sidebar.title('Year')
year = st.sidebar.selectbox('Select a year:', year_option, index=1)

# key metrics to be displayed on the side bar
metrics = helper.get_key_metrics(processed_data,year)

# metric card 1 --- Total Expenditure
st.sidebar.markdown(custom_css, unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class="custom-title">
    <p style="font-size: 18px;">Total Expenditure</p>
    <p style="font-size: 22px; font-weight: bold; margin: 0;">S$ {metrics[0]}</p>
</div>
""", unsafe_allow_html=True)

# metric card 2 --- Total Number of Orders
st.sidebar.markdown(custom_css, unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class="custom-title">
    <p style="font-size: 18px;">Total Number of Orders</p>
    <p style="font-size: 22px; font-weight: bold; margin: 0;">{metrics[1]} orders</p>
</div>
""", unsafe_allow_html=True)

# metric card 3 --- Most Expensive Expenses on the Year
st.sidebar.markdown(custom_css, unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class="custom-title">
    <p style="font-size: 18px;">Most Expensive Puchase</p>
    <p style="font-size: 22px; font-weight: bold; margin: 0;">Vendor: {metrics[2]} <br> Value: S$ {metrics[3]} </p>
</div>
""", unsafe_allow_html=True)

# metric card 4 --- Average Invoice Processing Time
st.sidebar.markdown(custom_css, unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class="custom-title">
    <p style="font-size: 18px;">Average Invoice Processing Time</p>
    <p style="font-size: 22px; font-weight: bold; margin: 0;">{metrics[4]} days</p>
</div>
""", unsafe_allow_html=True)

# metric card 5 --- Longest Invoice Processing Time
st.sidebar.markdown(custom_css, unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class="custom-title">
    <p style="font-size: 18px;">Longest Invoice Processing Time</p>
    <p style="font-size: 22px; font-weight: bold; margin: 0;">{metrics[5]} days</p>
</div>
""", unsafe_allow_html=True)

# Dashboard Title --- WBS: R571000058281
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(f"""
<div class="custom-title">
    <p style="font-size: 40px; font-weight: bold; margin: 0;">WBS: R-571-000-035-133</p>
</div>
""", unsafe_allow_html=True)
st.markdown('#### ')

# split the dashboard body into 3 columns
col1, col2, col3 = st.columns([2.8,3.2,2])

# Column 1 (2 plots)
# plot 1 --- heatmap for overview the expenses in the year selected by the user
col1.markdown(f'#### Overview of Expenses in {year}')
heatmap = helper.plot_heatmap(heatmap_data, year)
col1.plotly_chart(heatmap, theme='streamlit', use_container_width=True)
# plot 2 --- treemap for overview of expenses by category in the year selected by the user
col1.markdown(f'#### Expenses in {year} by Category')
treemap = helper.plot_treemap(processed_data, year)
col1.plotly_chart(treemap, theme='streamlit', use_container_width=True)

# Column 2 (1 plot)
# plot 1 --- bubble chart for overview the ovrall expenditure based on category and vendors
col2.markdown(f'#### Category-wise Expenditures by Vendors in {year}')
bubble = helper.plot_bubble(processed_data, year)
col2.plotly_chart(bubble, theme='streamlit', use_container_width=True)

# Column 3 (1 table)
# table 1 --- table to display the breakdown of the expenses spent based on vendor in the year selected by the user 
col3.markdown('#### Total Expenses by Vendors')
vendor_table = helper.vendor_by_expenses(processed_data, year)
vendor_table['Value'] = vendor_table['Value'].round(2)
col3.dataframe(vendor_table, height=1000, hide_index=True, use_container_width=True)
