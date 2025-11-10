
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title('2024 Polling Dashboard')

# --- Load Dataset ---
df = pd.read_csv('data/clean/generic_ballot_polls_dashboard.csv')
df['start_date'] = pd.to_datetime(df['start_date'])

# --- Compute margin and rolling averages ---
df['margin'] = df['dem'] - df['rep']
df['dem_roll7'] = df['dem'].rolling(7, min_periods=1).mean()
df['rep_roll7'] = df['rep'].rolling(7, min_periods=1).mean()
df['margin_roll7'] = df['margin'].rolling(7, min_periods=1).mean()

# --- Clean methodology ---
def clean_methodology(method):
    if pd.isna(method):
        return "unknown"
    method = method.lower()
    if "live phone" in method or ("text" in method and "text-to-web" not in method):
        return "phone"
    elif "online" in method or "text-to-web" in method:
        return "online"
    elif "probability" in method:
        return "panel"
    else:
        return "unknown"

df['methodology'] = df['methodology'].apply(clean_methodology)

# --- Sidebar Filters ---
st.sidebar.header('Filters')
date_range = st.sidebar.date_input(
    'Date Range',
    [df['start_date'].min(), df['start_date'].max()]
)
party_options = ['dem', 'rep']
selected_parties_margin = st.sidebar.multiselect(
    'Select Party(s) for Margin Series',
    options=party_options,
    default=party_options
)
selected_parties_hist = st.sidebar.multiselect(
    'Select Party(s) for Distribution',
    options=party_options,
    default=party_options
)
show_stats = st.sidebar.checkbox('Show mean & std deviation on histograms', value=True)

selected_pollsters_scatter = st.sidebar.multiselect(
    'Pollsters for Scatter',
    options=sorted(df['pollster'].dropna().unique()),
    default=sorted(df['pollster'].dropna().unique())
)
selected_methods_scatter = st.sidebar.multiselect(
    'Methodologies for Scatter',
    options=sorted(df['methodology'].dropna().unique()),
    default=sorted(df['methodology'].dropna().unique())
)

# --- Global Filters ---
df_filtered = df[
    (df['start_date'] >= pd.to_datetime(date_range[0])) &
    (df['start_date'] <= pd.to_datetime(date_range[1]))
].copy()

# --- KPIs ---
total_polls = len(df_filtered)
avg_margin = df_filtered['margin'].mean()
kpi_cols = st.columns(3)
kpi_cols[0].metric("Total Polls", total_polls)
kpi_cols[1].metric("Average Margin", f"{avg_margin:.2f}")
if 'predicted_margin' in df_filtered.columns:
    kpi_cols[2].metric("Average Predicted Margin", f"{df_filtered['predicted_margin'].mean():.2f}")

# --- Poll Margin Over Time ---
st.subheader('Poll Margin Over Time')
if selected_parties_margin:
    fig_margin = px.line(
        df_filtered,
        x='start_date',
        y=selected_parties_margin,
        title='Poll Support Over Time',
        height=600
    )
    fig_margin.add_scatter(
        x=df_filtered['start_date'],
        y=df_filtered['margin_roll7'],
        mode='lines',
        name='7-day Rolling Avg'
    )
    if 'predicted_margin' in df_filtered.columns:
        fig_margin.add_scatter(
            x=df_filtered['start_date'],
            y=df_filtered['predicted_margin'],
            mode='lines',
            name='Predicted Margin'
        )
    st.plotly_chart(fig_margin, use_container_width=True)
else:
    st.info("Select at least one party to show.")

# --- Distribution of Support ---
st.subheader('Distribution of Support')
if selected_parties_hist:
    hist_data = df_filtered[selected_parties_hist].melt(var_name='party', value_name='support')
    fig_hist = px.histogram(
        hist_data,
        x='support',
        color='party',
        barmode='overlay',
        nbins=20,
        title='Distribution of Party Support',
        height=500
    )
    if show_stats:
        for party in selected_parties_hist:
            mean_val = df_filtered[party].mean()
            std_val = df_filtered[party].std()
            fig_hist.add_vline(x=mean_val, line_dash='dash', annotation_text=f"{party} mean")
            fig_hist.add_vline(x=mean_val + std_val, line_dash='dot', annotation_text=f"{party} +1 std")
            fig_hist.add_vline(x=mean_val - std_val, line_dash='dot', annotation_text=f"{party} -1 std")
    st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.info("Select at least one party to show.")

# --- Pollster Counts & Average Margin ---
st.subheader("Pollster Counts & Average Margin")
pollster_counts = df_filtered.groupby('pollster').agg(count=('margin','size'), avg_margin=('margin','mean')).reset_index()
fig_pollster = px.bar(
    pollster_counts,
    x='pollster',
    y='count',
    color='avg_margin',
    title='Pollster Counts & Avg Margin',
    height=500,
    text='count'
)
st.plotly_chart(fig_pollster, use_container_width=True)

# --- Methodology Counts & Average Margin ---
st.subheader("Methodology Counts & Average Margin")
method_counts = df_filtered.groupby('methodology').agg(count=('margin','size'), avg_margin=('margin','mean')).reset_index()
fig_method = px.bar(
    method_counts,
    x='methodology',
    y='count',
    color='avg_margin',
    title='Methodology Counts & Avg Margin',
    height=500,
    text='count'
)
st.plotly_chart(fig_method, use_container_width=True)

# --- Sample Size vs Margin Scatter ---
st.subheader("Sample Size vs Margin")
df_scatter = df_filtered[
    df_filtered['pollster'].isin(selected_pollsters_scatter) &
    df_filtered['methodology'].isin(selected_methods_scatter)
]
fig_scatter = px.scatter(
    df_scatter,
    x='sample_size',
    y='margin',
    color='pollster',
    symbol='methodology',
    size='sample_size',
    hover_data=['pollster', 'methodology'],
    title='Sample Size vs Margin',
    height=700
)
st.plotly_chart(fig_scatter, use_container_width=True)
