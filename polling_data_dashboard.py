
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('data/clean/generic_ballot_polls_clean.csv')
df['start_date'] = pd.to_datetime(df['start_date'])

st.title('2024 Polling Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
pollsters = st.sidebar.multiselect('Select Pollsters', options=df['pollster'].unique(), default=df['pollster'].unique())
methodologies = st.sidebar.multiselect('Select Methodologies', options=df['methodology'].unique(), default=df['methodology'].unique())
date_range = st.sidebar.date_input('Date Range', [df['start_date'].min(), df['start_date'].max()])

# Filter dataframe
df_filtered = df[
    (df['pollster'].isin(pollsters)) &
    (df['methodology'].isin(methodologies)) &
    (df['start_date'] >= pd.to_datetime(date_range[0])) &
    (df['start_date'] <= pd.to_datetime(date_range[1]))
]

# Time series: margin & rolling average
st.subheader('Poll Margin Over Time')
fig_margin = px.line(df_filtered, x='start_date', y='margin', title='Poll Margin Over Time')
fig_margin.add_scatter(x=df_filtered['start_date'], y=df_filtered['margin_roll7'], mode='lines', name='7-day Rolling Avg')
st.plotly_chart(fig_margin)

# Predicted margin if available
if 'predicted_margin' in df_filtered.columns:
    st.subheader('Predicted Margin Over Time')
    fig_pred = px.line(df_filtered, x='start_date', y='predicted_margin', title='Predicted Margin Over Time')
    st.plotly_chart(fig_pred)

# Histograms
st.subheader('Distribution of Democratic and Republican Support')
fig_hist = px.histogram(df_filtered.melt(id_vars=[], value_vars=['dem','rep']), x='value', color='variable', barmode='overlay')
st.plotly_chart(fig_hist)

# Pollster analysis
st.subheader('Pollster Counts')
st.bar_chart(df_filtered['pollster'].value_counts())

st.subheader('Pollster Average Margin')
pollster_avg = df_filtered.groupby('pollster')['margin'].mean().sort_values()
st.bar_chart(pollster_avg)

# Methodology analysis
st.subheader('Methodology Counts')
st.bar_chart(df_filtered['methodology'].value_counts())

st.subheader('Methodology Average Margin')
method_avg = df_filtered.groupby('methodology')['margin'].mean().sort_values()
st.bar_chart(method_avg)

# Sample size effect
st.subheader('Sample Size vs Margin')
fig_scatter = px.scatter(df_filtered, x='sample_size', y='margin', color='pollster', size='sample_size', title='Sample Size Effect')
st.plotly_chart(fig_scatter)
