import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder

# Load the CSV data or use example data if file load fails
try:
    data = pd.read_csv('/mnt/data/alerts.csv')
    data['timestamp'] = pd.to_datetime(data['timestamp'])
except:
    # Example data if CSV not loaded
    data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'severity': np.random.choice(['Low', 'Medium', 'High'], size=100),
        'alert_type': np.random.choice(['Port Scan', 'Brute Force', 'DDoS', 'Malware'], size=100),
        'source': np.random.choice(['192.168.1.1', '192.168.1.2', '10.0.0.1', '10.0.0.2'], size=100),
        'destination': np.random.choice(['192.168.1.3', '192.168.1.4', '10.0.0.3', '10.0.0.4'], size=100),
    })

# Title with main logo (optional)
st.title("🔒 Network Intrusion Detection System (NIDS) Dashboard with AI/ML")

# Model Performance Metrics with Icons
st.header("Model Performance Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.write("🎯")
col1.metric("Accuracy", "95.0%")
col2.write("📏")
col2.metric("Precision", "92.0%")
col3.write("🔄")
col3.metric("Recall", "89.0%")
col4.write("🏆")
col4.metric("F1 Score", "90.0%")

# Custom Alerts Table with AgGrid
st.header("📊 Anomaly/Security Alerts")

# Set up AgGrid options for better styling
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
gb.configure_side_bar()  # Add a sidebar with filters
gb.configure_default_column(editable=False, groupable=True, wrapText=True)  # Wrap text to make content visible
gb.configure_column("severity", cellStyle={"color": "black", "backgroundColor": "lightcoral"})
gb.configure_column("alert_type", cellStyle={"color": "black", "backgroundColor": "lightblue"})
gb.configure_column("source", cellStyle={"color": "black", "backgroundColor": "lightyellow"})
gb.configure_column("destination", cellStyle={"color": "black", "backgroundColor": "lightgreen"})

grid_options = gb.build()
AgGrid(data, gridOptions=grid_options, theme="material", height=400, fit_columns_on_grid_load=True)

# Traffic Analysis with Icon
st.header("📈 Traffic Analysis")

if 'timestamp' in data.columns:
    traffic_count = data.groupby(data['timestamp'].dt.date).size()
    st.line_chart(traffic_count, width=0, height=400)

# Severity Distribution
if 'severity' in data.columns:
    st.subheader("Severity Distribution of Alerts")
    severity_counts = data['severity'].value_counts()
    st.bar_chart(severity_counts)

# Source/Destination Analysis
if 'source' in data.columns and 'destination' in data.columns:
    st.subheader("Top Sources and Destinations")
    top_sources = data['source'].value_counts().head(5)
    top_destinations = data['destination'].value_counts().head(5)
    col5, col6 = st.columns(2)
    with col5:
        st.bar_chart(top_sources)
    with col6:
        st.bar_chart(top_destinations)

# Additional options
if st.checkbox("Show Detailed Data Summary"):
    st.write(data.describe())
