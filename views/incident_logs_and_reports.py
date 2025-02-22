import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Database connection
DATABASE_FILE = "emergency_management.db"

# Fixing the incorrect parameter binding issue and reinserting dummy data

# Connect to the database
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Insert new dummy incidents
cursor.executemany("""
    INSERT INTO incidents (type, description, lat, lon, responders_needed, timestamp)
    VALUES (?, ?, ?, ?, ?, datetime('now', ?))
""", [
    ("Fire", "House fire reported in central area", 40.75, -74.05, 3, "-1 day"),
    ("Medical", "Person unconscious near park", 40.71, -74.01, 2, "-2 days"),
    ("Accident", "Car accident near main highway", 40.72, -74.02, 4, "-3 days"),
    ("Other", "Electrical hazard in shopping mall", 40.73, -74.03, 2, "-4 days"),
    ("Fire", "Warehouse on fire", 40.76, -74.06, 5, "-5 days"),
    ("Medical", "Injury reported near school", 40.74, -74.04, 1, "-6 days"),
    ("Fire", "Forest fire detected", 40.78, -74.08, 7, "-7 days"),
    ("Accident", "Multiple vehicle collision", 40.79, -74.09, 6, "-8 days"),
    ("Medical", "Emergency at senior care center", 40.70, -74.00, 3, "-9 days"),
    ("Other", "Gas leak reported", 40.71, -74.02, 4, "-10 days")
])

# Commit changes and close connection
conn.commit()
conn.close()


def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    return conn


# Load incident data
def load_incidents():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()

    # Convert timestamp column to datetime format
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

    return df


# Export as CSV
def export_csv(df):
    df.to_csv("incident_reports.csv", index=False)
    st.success("✅ Incident report exported as CSV!")


# Export as PDF (Placeholder for implementation)
def export_pdf():
    st.warning("📄 PDF export feature coming soon!")


# Incident Logs Page
def incident_logs():
    st.title("Incident Logs & Reports")

    # Load incident data
    df = load_incidents()

    # Ensure timestamp is in datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Incidents")

    # Handle missing timestamps
    min_date = df["timestamp"].min() if not df["timestamp"].isna().all() else pd.to_datetime("today")
    max_date = df["timestamp"].max() if not df["timestamp"].isna().all() else pd.to_datetime("today")

    # Date Range Filter
    start_date = st.sidebar.date_input("Start Date", min_date.date())
    end_date = st.sidebar.date_input("End Date", max_date.date())

    # Incident Type Filter
    incident_type = st.sidebar.selectbox("Select Type:", ["All"] + list(df["type"].dropna().unique()))

    # Status Filter
    status = st.sidebar.selectbox("Select Status:", ["All", "Ongoing", "Resolved"])

    # Apply filters
    df = df[(df["timestamp"] >= pd.to_datetime(start_date)) & (df["timestamp"] <= pd.to_datetime(end_date))]

    if incident_type != "All":
        df = df[df["type"] == incident_type]
    if status != "All":
        df = df[df["status"] == status]

    # Search Bar for Incidents
    search_query = st.text_input("🔍 Search by Type", "")
    if search_query:
        df = df[df.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]

    # Display filtered incident table
    st.write("### Incident Logs")
    st.dataframe(df)

    # Incident Statistics & Charts
    st.write("### 📊 Incident Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incidents by Type")
        if not df.empty:
            type_count = df["type"].value_counts().reset_index()
            type_count.columns = ["Incident Type", "Count"]
            fig = px.bar(type_count, x="Incident Type", y="Count", labels={"x": "Incident Type", "y": "Count"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for this filter.")

    with col2:
        st.subheader("Incidents Over Time")
        if not df.empty:
            df["date"] = df["timestamp"].dt.date
            date_count = df.groupby("date").size().reset_index(name="Incident Count")
            fig2 = px.line(date_count, x="date", y="Incident Count", labels={"x": "Date", "y": "Number of Incidents"})
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("No data available for this filter.")

    # Export options
    st.write("### Export Reports")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export as CSV"):
            export_csv(df)
    with col2:
        if st.button("📄 Export as PDF"):
            export_pdf()


incident_logs()
