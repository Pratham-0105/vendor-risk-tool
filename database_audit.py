import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Vendor Risk Command Center",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE vendor_assessments (
        vendor_id TEXT PRIMARY KEY,
        vendor_name TEXT,
        risk_tier TEXT,
        service_type TEXT
    );
    """
)

cursor.executescript(
    """
    INSERT INTO vendor_assessments VALUES ('V01', 'CloudCorp', 'Critical', 'Cloud Hosting');
    INSERT INTO vendor_assessments VALUES ('V02', 'DataSync', 'High', 'Data Analytics');
    INSERT INTO vendor_assessments VALUES ('V03', 'PaySecure', 'Critical', 'Payment Gateway');
    INSERT INTO vendor_assessments VALUES ('V04', 'StaffCo', 'Medium', 'HR Portal');
    INSERT INTO vendor_assessments VALUES ('V05', 'LogiTrack', 'Low', 'Logistics');
    INSERT INTO vendor_assessments VALUES ('V06', 'NetGuard', 'High', 'Managed Security');
    """
)
conn.commit()

df_assessments = pd.read_sql_query(
    "SELECT vendor_id, vendor_name, risk_tier, service_type FROM vendor_assessments;",
    conn,
)

color_map = {
    "Critical": "#d94f45",
    "High": "#ed8b43",
    "Medium": "#e7b84b",
    "Low": "#2b9c8f",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #20333a;
        --muted: #728087;
        --paper: #f7f8f5;
        --line: #dde5e1;
        --teal: #2b9c8f;
        --coral: #d94f45;
    }

    .stApp { background: var(--paper); color: var(--ink); }
    .block-container { padding: 2.2rem 3.5rem 3rem; max-width: 1500px; }
    [data-testid="stSidebar"] { background: #20333a; border-right: 0; }
    [data-testid="stSidebar"] * { color: #edf4f1; }
    [data-testid="stSidebar"] .stRadio label { color: #d3e1dd; }
    [data-testid="stSidebar"] hr { border-color: #48615f; }
    h1, h2, h3, p, div, span, label { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--ink); }
    h1 { letter-spacing: -0.5px; font-size: 2.45rem !important; margin-bottom: 0.2rem; }
    h2 { font-size: 1.25rem !important; }
    .eyebrow { color: var(--teal); font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
    .subtitle { color: var(--muted); font-size: 1rem; margin-bottom: 1.8rem; }
    .metric-card { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 1.1rem 1.25rem; min-height: 112px; box-shadow: 0 4px 18px rgba(32, 51, 58, 0.045); }
    .metric-label { color: var(--muted); font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; }
    .metric-value { color: var(--ink); font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; margin-top: 0.55rem; }
    .metric-note { color: var(--muted); font-size: 0.78rem; margin-top: 0.2rem; }
    .section-head { align-items: baseline; display: flex; justify-content: space-between; margin: 2rem 0 0.75rem; }
    .section-head h2 { margin: 0; }
    .section-note { color: var(--muted); font-size: 0.82rem; }
    .status-pill { border-radius: 20px; display: inline-block; font-size: 0.75rem; font-weight: 700; padding: 0.35rem 0.7rem; }
    .status-critical { background: #fbe8e6; color: #a9362e; }
    .status-high { background: #fff0e4; color: #a85b1f; }
    .status-medium { background: #fff6d9; color: #846512; }
    .status-low { background: #e1f3ef; color: #1d756b; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## VENDOR\n## RISK OPS")
    st.caption("Security posture workspace")
    st.divider()
    st.markdown("### View controls")
    selected_tiers = st.multiselect(
        "Risk tiers",
        options=["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium", "Low"],
    )
    st.divider()
    st.markdown("### Data health")
    st.success("Live sample feed\n\nSQLite in-memory")
    st.caption("Last refreshed: just now")

filtered_df = df_assessments[df_assessments["risk_tier"].isin(selected_tiers)]
risk_counts = (
    filtered_df.groupby("risk_tier", as_index=False)
    .size()
    .rename(columns={"size": "total_vendors"})
)
risk_counts["risk_tier"] = pd.Categorical(
    risk_counts["risk_tier"],
    categories=["Critical", "High", "Medium", "Low"],
    ordered=True,
)
risk_counts = risk_counts.sort_values("risk_tier")

st.markdown('<div class="eyebrow">Third-party security oversight</div>', unsafe_allow_html=True)
st.title("Vendor Risk Command Center")
st.markdown(
    '<div class="subtitle">A concise view of vendor exposure, risk concentration and review priorities.</div>',
    unsafe_allow_html=True,
)

metric_columns = st.columns(4)
metrics = [
    ("Vendors monitored", len(filtered_df), "Across selected tiers"),
    ("Critical exposure", int((filtered_df["risk_tier"] == "Critical").sum()), "Immediate review focus"),
    ("Elevated exposure", int(filtered_df["risk_tier"].isin(["Critical", "High"]).sum()), "Critical + high risk"),
    ("Service categories", filtered_df["service_type"].nunique(), "Unique vendor services"),
]
for column, (label, value, note) in zip(metric_columns, metrics):
    with column:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="section-head"><h2>Risk distribution</h2><span class="section-note">Grouped with SQL COUNT(*)</span></div>',
    unsafe_allow_html=True,
)

chart_column, priority_column = st.columns([1.15, 0.85], gap="large")
with chart_column:
    if risk_counts.empty:
        st.info("Select at least one risk tier from the sidebar.")
    else:
        figure = px.pie(
            risk_counts,
            values="total_vendors",
            names="risk_tier",
            color="risk_tier",
            color_discrete_map=color_map,
            hole=0.68,
        )
        figure.update_traces(
            textinfo="percent",
            textfont_size=13,
            marker={"line": {"color": "#f7f8f5", "width": 4}},
            hovertemplate="%{label}: %{value} vendor(s)<extra></extra>",
        )
        figure.update_layout(
            height=365,
            margin={"t": 20, "b": 20, "l": 10, "r": 10},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend={"orientation": "h", "y": -0.04, "x": 0.1},
            font={"family": "DM Sans", "color": "#20333a"},
            annotations=[{"text": f"{len(filtered_df)}<br><span style='font-size:12px'>vendors</span>", "showarrow": False, "font": {"size": 24, "color": "#20333a"}}],
        )
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})

with priority_column:
    st.markdown("#### Review priority")
    st.caption("Vendors needing the fastest security follow-up")
    priority_df = filtered_df[filtered_df["risk_tier"].isin(["Critical", "High"])].copy()
    priority_df["Priority"] = priority_df["risk_tier"].map({"Critical": "P1", "High": "P2"})
    priority_df = priority_df.sort_values("Priority")
    if priority_df.empty:
        st.info("No critical or high-risk vendors in the current view.")
    else:
        st.dataframe(
            priority_df[["Priority", "vendor_name", "risk_tier", "service_type"]].rename(
                columns={"vendor_name": "Vendor", "risk_tier": "Risk tier", "service_type": "Service"}
            ),
            hide_index=True,
            width="stretch",
            height=245,
            column_config={"Priority": st.column_config.TextColumn("Priority", width="small")},
        )

st.markdown(
    '<div class="section-head"><h2>Vendor register</h2><span class="section-note">Current assessment inventory</span></div>',
    unsafe_allow_html=True,
)
st.dataframe(
    filtered_df.rename(
        columns={
            "vendor_id": "ID",
            "vendor_name": "Vendor",
            "risk_tier": "Risk tier",
            "service_type": "Service category",
        }
    ),
    hide_index=True,
    width="stretch",
    column_config={
        "Risk tier": st.column_config.TextColumn("Risk tier"),
        "ID": st.column_config.TextColumn("ID", width="small"),
    },
)

st.caption("Source: vendor_assessments | Query pattern: GROUP BY risk_tier, COUNT(*) | Demo data is held in memory for this dashboard.")
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
