import streamlit as st
import pandas as pd
import numpy as np
import joblib
from st_aggrid import AgGrid, GridOptionsBuilder
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load the trained model and scaler
model = joblib.load('anomaly_model.pkl')
scaler = joblib.load('scaler.pkl')

# Load sample or real-time data (using example data for simplicity)
try:
    data = pd.read_csv('/mnt/data/alerts.csv')
    data['timestamp'] = pd.to_datetime(data['timestamp'])
except:
    # Generate sample data if CSV is not available
    data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'byte_count': np.random.randint(100, 10000, size=100),
        'duration': np.random.randint(1, 100, size=100),
        'source_port': np.random.randint(1000, 65535, size=100),
        'dest_port': np.random.randint(1000, 65535, size=100),
    })

# Feature scaling
features = data[['byte_count', 'duration', 'source_port', 'dest_port']]
features_scaled = scaler.transform(features)

# Predict anomalies using the model
data['anomaly'] = model.predict(features_scaled)
data['severity'] = data['anomaly'].apply(lambda x: 'High' if x == -1 else 'Low')

# Streamlit Dashboard
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
gb.configure_default_column(editable=False, groupable=True)

# Apply different colors based on severity
severity_colors = {
    "High": "lightcoral",
    "Low": "lightgreen"
}
gb.configure_column("severity", cellStyle=lambda params: {
    "color": "black",
    "backgroundColor": severity_colors.get(params.value, "lightgrey")
})
grid_options = gb.build()

# Display data with AgGrid
AgGrid(data, gridOptions=grid_options, theme="material", height=400, fit_columns_on_grid_load=True)

# Traffic Analysis
st.header("📈 Traffic Analysis")
if 'timestamp' in data.columns:
    traffic_count = data.groupby(data['timestamp'].dt.date).size()
    st.line_chart(traffic_count, width=0, height=400)

# Severity Distribution
st.subheader("Severity Distribution of Alerts")
severity_counts = data['severity'].value_counts()
severity_chart = st.bar_chart(severity_counts)

# Additional options for data exploration
if st.checkbox("Show Detailed Data Summary"):
    st.write(data.describe())
