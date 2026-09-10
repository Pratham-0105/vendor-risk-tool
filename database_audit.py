import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# STEP 1: INITIALIZE IN-MEMORY SQL DATABASE & SAMPLE DATA
# =========================================================

# This establishes a live, isolated SQL database completely in your VM's RAM
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create your vendor assessment table schema
cursor.execute("""
CREATE TABLE vendor_assessments (
    vendor_id TEXT PRIMARY KEY,
    vendor_name TEXT,
    risk_tier TEXT,
    service_type TEXT
);
""")

# Populate the table with sample vendor compliance data
cursor.executescript("""
INSERT INTO vendor_assessments VALUES ('V01', 'CloudCorp', 'Critical', 'Cloud Hosting');
INSERT INTO vendor_assessments VALUES ('V02', 'DataSync', 'High', 'Data Analytics');
INSERT INTO vendor_assessments VALUES ('V03', 'PaySecure', 'Critical', 'Payment Gateway');
INSERT INTO vendor_assessments VALUES ('V04', 'StaffCo', 'Medium', 'HR Portal');
INSERT INTO vendor_assessments VALUES ('V05', 'LogiTrack', 'Low', 'Logistics');
INSERT INTO vendor_assessments VALUES ('V06', 'NetGuard', 'High', 'Managed Security');
""")
conn.commit()

# =========================================================
# STEP 2: RUN THE SQL GROUP BY & COUNT QUERY
# =========================================================

# The exact ANSI SQL query logic
sql_query = """
    SELECT risk_tier, COUNT(*) as total_vendors
    FROM vendor_assessments
    GROUP BY risk_tier
    ORDER BY total_vendors DESC;
"""

# Execute SQL query and load the results directly into a Pandas DataFrame
df_metrics = pd.read_sql_query(sql_query, conn)

# =========================================================
# STEP 3: BUILD THE INTERACTIVE COLORFUL PIE CHART
# =========================================================

st.title("📊 Vendor Risk Density Audit Engine")
st.markdown("This dashboard extracts real-time database metrics using `GROUP BY` and `COUNT(*)` expressions.")

# Define explicit high-contrast GRC colors for the risk tiers
color_map = {
    'Critical': '#D9381E',  # Red
    'High': '#F28E2B',      # Orange
    'Medium': '#F1CE63',    # Yellow
    'Low': '#4E79A7'        # Blue
}

# Generate the pie/donut chart view
fig = px.pie(
    df_metrics, 
    values='total_vendors', 
    names='risk_tier', 
    color='risk_tier',
    color_discrete_map=color_map,
    hole=0.4,
    title='Vendor Threat Profile Density'
)

# Render components to the web interface
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Raw SQL Output Table:")
st.dataframe(df_metrics)
