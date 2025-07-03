import streamlit as st
import us
import plotly.express as px
import pandas as pd
from datetime import datetime

st.title("US monthly beverage sales per state (2010-2011)")
df_sales = pd.read_csv('sales_USA_2010_2011.csv')

#convert Date to datetime type
df_sales['Date'] = pd.to_datetime(df_sales['Date'], format='%m/%d/%y %H:%M:%S')

#create a Year-Month column
df_sales['Month'] = df_sales['Date'].dt.to_period('M').astype(str)
months = sorted({d.strftime('%Y-%m') for d in pd.to_datetime(df_sales['Date'])})

#replace full names of states with 2-character abbreviations
df_sales['State'] = df_sales['State'] = df_sales['State'].apply(lambda x: us.states.lookup(x).abbr if us.states.lookup(x) else None)

#select product
product_category_options = ['All'] + sorted({ptype for ptype in df_sales['Product Type'] if pd.notnull(ptype)})
selected_product_category = st.selectbox("Select Product Category:", product_category_options, index=2)

#slider for months
selected_month = st.select_slider('Pick a month:', options=months, value='2010-06')

#narrow down the data for display
df_filtered = df_sales[df_sales['Month'] == selected_month]
if selected_product_category != 'All':
    df_filtered = df_filtered[df_filtered['Product Type'] == selected_product_category]


df_aggregated = df_filtered.groupby('State', as_index=False)['Sales'].sum()

#choropleth
fig = px.choropleth(df_aggregated,
                    locations='State',
                    locationmode='USA-states',
                    color='Sales',
                    scope='usa',
                    color_continuous_scale='Reds',
                    labels={'Sales':'Sales Amount'})


st.plotly_chart(fig)