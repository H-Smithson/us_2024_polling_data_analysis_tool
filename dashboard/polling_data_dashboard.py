
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('data/clean/generic_ballot_polls_dashboard.csv')
df['start_date'] = pd.to_datetime(df['start_date'])

st.title('2024 Polling Dashboard')

# --- Sidebar Filters ---
st.sidebar.header('Filters')

# Pollster multi-select
pollster_options = df['pollster'].unique()
selected_pollsters = st.sidebar.multiselect('Select Pollster(s)', options=pollster_options, default=pollster_options)

# Methodology multi-select
methodology_options = df['methodology'].unique()
selected_methods = st.sidebar.multiselect('Select Methodology(s)', options=methodology_options, default=methodology_options)

# Date range
date_range = st.sidebar.date_input('Date Range', [df['start_date'].min(), df['start_date'].max()])

# Party selection for charts
party_options = ['dem', 'rep']
selected_parties_margin = st.sidebar.multiselect('Select Party(s) for Margin', party_options, default=party_options)
selected_parties_hist = st.sidebar.multiselect('Select Party(s) for Distribution', party_options, default=party_options)

# Toggle for showing mean and std deviation in histogram
show_stats = st.sidebar.checkbox('Show mean and std deviation on distribution', value=True)

# --- Filter DataFrame ---
df_filtered = df[
    (df['pollster'].isin(selected_pollsters)) &
    (df['methodology'].isin(selected_methods)) &
    (df['start_date'] >= pd.to_datetime(date_range[0])) &
    (df['start_date'] <= pd.to_datetime(date_range[1]))
]

# --- Poll Margin Over Time ---
st.subheader('Poll Margin Over Time')
fig_margin = px.line(df_filtered, x='start_date', y=selected_parties_margin, title='Poll Margin Over Time')
fig_margin.add_scatter(x=df_filtered['start_date'], y=df_filtered['margin_roll7'], mode='lines', name='7-day Rolling Avg')
st.plotly_chart(fig_margin)

# --- Predicted Margin ---
if 'predicted_margin' in df_filtered.columns:
    st.subheader('Predicted Margin Over Time')
    fig_pred = px.line(df_filtered, x='start_date', y='predicted_margin', title='Predicted Margin Over Time')
    st.plotly_chart(fig_pred)

# --- Distribution of Support ---
st.subheader('Distribution of Support')
hist_data = df_filtered[selected_parties_hist].melt(var_name='party', value_name='support')
fig_hist = px.histogram(hist_data, x='support', color='party', barmode='overlay', nbins=20)

if show_stats:
    for party in selected_parties_hist:
        mean_val = df_filtered[party].mean()
        std_val = df_filtered[party].std()
        fig_hist.add_vline(x=mean_val, line_dash='dash', line_color='blue', annotation_text=f"{party} mean")
        fig_hist.add_vline(x=mean_val + std_val, line_dash='dot', line_color='green', annotation_text=f"{party} +1 std")
        fig_hist.add_vline(x=mean_val - std_val, line_dash='dot', line_color='green', annotation_text=f"{party} -1 std")

st.plotly_chart(fig_hist)

# --- Pollster Average Margin ---
st.subheader('Pollster Average Margin')
pollster_avg = df_filtered.groupby('pollster')['margin'].mean().sort_values()
pollster_avg_selected = pollster_avg.loc[selected_pollsters]
st.bar_chart(pollster_avg_selected)

# --- Methodology Average Margin ---
st.subheader('Methodology Average Margin')
method_avg = df_filtered.groupby('methodology')['margin'].mean().sort_values()
method_avg_selected = method_avg.loc[selected_methods]
st.bar_chart(method_avg_selected)

# --- Sample Size vs Margin ---
st.subheader('Sample Size vs Margin')
fig_scatter = px.scatter(
    df_filtered, x='sample_size', y='margin', color='pollster', size='sample_size',
    hover_data=['methodology'], title='Sample Size vs Margin'
)
st.plotly_chart(fig_scatter)
