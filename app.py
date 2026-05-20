import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------- Load Data --------------------
@st.cache_data
def load_data():
    df = pd.read_excel("classified_translations.xlsx")

    # Force datetime conversion
    df['Date of Accident'] = pd.to_datetime(df['Date of Accident'], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=['Date of Accident'])

    # Extract Month only
    df['Month'] = df['Date of Accident'].dt.month

    # If there's a column like "FY23", "FY24", use that instead of datetime-based year
    df['Financial Year'] = df['Year'].astype(str).str.upper().str.replace(" ", "")

    return df

df = load_data()

# -------------------- Title --------------------
st.set_page_config(page_title="Accident Dashboard", layout="wide")
st.title("⚡ Accident Data Dashboard")

# -------------------- Sidebar Filters --------------------
st.sidebar.header("🔍 Filter Data")

# Year Filter
# years = sorted(df['Financial Year'].dropna().unique(), reverse=True)
years = ["FY22","FY23","FY24","FY25"]
selected_years = st.sidebar.multiselect("Select Financial Year(s)", options=years, default=years)

# Circle Filter
circles = df['Circle'].dropna().unique()
selected_circles = st.sidebar.multiselect("Select Circle(s)", options=circles, default=circles)

# Employee Type Filter
emp_types = df['Employee Type'].dropna().unique()
selected_emp_types = st.sidebar.multiselect("Select Employee Type(s)", options=emp_types, default=emp_types)

# DISCOM Filter
discoms = df['DISCOM'].dropna().unique()
selected_discoms = st.sidebar.multiselect("Select DISCOM(s)", options=discoms, default=discoms)

# -------------------- Filtered Data --------------------
filtered_df = df[
    df['Financial Year'].isin(selected_years) &
    df['Circle'].isin(selected_circles) &
    df['Employee Type'].isin(selected_emp_types) &
    df['DISCOM'].isin(selected_discoms)
]

# -------------------- KPIs --------------------
st.subheader("📊 Summary Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Accidents", len(filtered_df))
col2.metric("Unique Circles", filtered_df['Circle'].nunique())
col3.metric("Employee Types", filtered_df['Employee Type'].nunique())

# -------------------- Bar Charts --------------------
st.subheader("📍 Accidents by Circle")
circle_counts = filtered_df['Circle'].value_counts()
st.bar_chart(circle_counts)

st.subheader("📍 Accidents by Sub-Division (Top 15)")
top_subdiv = filtered_df['Sub-Division'].value_counts().head(15)
st.bar_chart(top_subdiv)

st.subheader("⚠️ Nature of Accidents")
nature_counts = filtered_df['Nature of Accident'].value_counts()
st.bar_chart(nature_counts)

# -------------------- Yearly Trend --------------------
st.subheader("📈 Yearly Trend of Accidents")
fy_counts = filtered_df['Financial Year'].value_counts().sort_index()
st.line_chart(fy_counts)

# -------------------- Monthly Trend Across FYs --------------------
st.subheader("📆 Monthly Trend Across Financial Years")
monthly = filtered_df.groupby(['Financial Year', 'Month']).size().unstack(fill_value=0)
st.line_chart(monthly.T)

# -------------------- Employee Type Pie Chart --------------------
st.subheader("👷‍♂️ Employee Type Distribution")
if not filtered_df.empty:
    emp_counts = filtered_df['Employee Type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(emp_counts, labels=emp_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")

# -------------------- Heatmap --------------------
st.subheader("📉 Heatmap: Circle vs Nature of Accident")
if not filtered_df.empty:
    heatmap_data = pd.crosstab(filtered_df['Circle'], filtered_df['Nature of Accident'])

    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale='YlGnBu',
        labels=dict(x="Nature of Accident", y="Circle", color="Count"),
        aspect='auto',
    )
    fig.update_traces(hovertemplate="Count: %{z}<br>Accident: %{x}<br>Circle: %{y}")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for heatmap based on current filters.")
