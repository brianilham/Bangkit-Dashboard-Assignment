import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataframe.
df = pd.read_csv("new_order_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# --- Styling ---
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff; 
    }
    .stSidebar {
        background-color: #00000;
    }
    h1 {
        color: #262730;
        font-size: 24px;
    }
    h2 {
        color: #262730;
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Dashboard ---
st.title("Bike Sharing Dashboard")

# --- Sidebar ---
st.sidebar.title("Filters")
weather_options = df['weathersit_y'].unique()
selected_weather = st.sidebar.multiselect(
    "Select Weather Type", weather_options, weather_options
)

cluster_options = df['cluster'].unique()
selected_cluster = st.sidebar.multiselect(
    "Select Cluster", cluster_options, cluster_options
)
start_date, end_date = st.sidebar.date_input(
    "Date Range", [df['dteday'].min(), df['dteday'].max()]
)

# --- Filter Data ---
filtered_df = df[
    df['weathersit_y'].isin(selected_weather)
    & df['cluster'].isin(selected_cluster)
    & (df['dteday'] >= pd.to_datetime(start_date))
    & (df['dteday'] <= pd.to_datetime(end_date))
]

# --- Correlation between temperature and bike rentals ---
st.header("Temperature vs. Rentals")
correlation = filtered_df['temp_y'].corr(filtered_df['cnt_y'])
st.write(f"Correlation: {correlation:.2f}")
plt.xlabel("Temperature")
plt.ylabel("Count of Bike Rentals")

# --- Scatter Plot ---
fig, ax = plt.subplots(figsize=(8, 4))
sns.regplot(
    x='temp_y',
    y='cnt_y',
    data=filtered_df,
    ax=ax,
    scatter_kws={'alpha': 0.6},
    line_kws={'color': '#262730'},
)
plt.xlabel("Normalized Temperature", fontsize=12)
plt.ylabel("Total Bike Rentals", fontsize=12)
st.pyplot(fig)

# --- Weather Type vs. Rentals ---
st.header("Weather Type vs. Rentals")
weather_rentals = filtered_df.groupby('weathersit_y')['cnt_y'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    x='weathersit_y', y='cnt_y', data=weather_rentals, ax=ax, color='#636EFA'
)
plt.xlabel(
    "Weather Type (1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain/Snow)",
    fontsize=12,
)
plt.ylabel("Average Bike Rentals", fontsize=12)
st.pyplot(fig)

# --- Cluster Visualization ---
st.header("Cluster Visualization")
fig, ax = plt.subplots(figsize=(8, 4))
sns.scatterplot(
    x='temp_y',
    y='cnt_y',
    hue='cluster',
    data=filtered_df,
    ax=ax,
    palette="deep",
    alpha=0.6,
)
plt.xlabel("Normalized Temperature", fontsize=12)
plt.ylabel("Total Bike Rentals", fontsize=12)
st.pyplot(fig)

