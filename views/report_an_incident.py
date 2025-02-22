import streamlit as st
import pandas as pd
import sqlite3
import geopy.distance


# Database setup
DATABASE_FILE = "incidents.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            description TEXT,
            lat REAL,
            lon REAL,
            responders_needed INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn, cursor


def save_incident(incident_data):
    conn, cursor = get_db_connection()
    cursor.execute("""
        INSERT INTO incidents (type, description, lat, lon, responders_needed)
        VALUES (?, ?, ?, ?, ?)""",
                   (incident_data["type"], incident_data["description"],
                    incident_data["lat"], incident_data["lon"], incident_data["responders_needed"])
                   )
    conn.commit()
    conn.close()


@st.cache_data
def load_responders():
    df = pd.read_csv("responders.csv")  # Replace with actual CSV file path
    return df


def get_nearby_responders(user_location, responders_df, max_distance, counts):
    nearby_responders = []
    counts_tracker = {"Police": 0, "Firefighter": 0, "Volunteer": 0}

    for _, row in responders_df.iterrows():
        responder_location = (row['lat'], row['lon'])
        distance = geopy.distance.geodesic(user_location, responder_location).km
        if distance <= max_distance and counts_tracker[row['Role']] < counts[row['Role']]:
            nearby_responders.append(row)
            counts_tracker[row['Role']] += 1

    return pd.DataFrame(nearby_responders)


def report_incident():
    st.title("🚨 Report an Incident")
    st.write("Fill in the details below to report an emergency incident.")

    # Incident Type Selection
    incident_type = st.selectbox("Select the type of incident:",
                                 ["Fire", "Accident", "Medical", "Other"])

    if incident_type == "Other":
        incident_type = st.text_input("Specify the type of incident:")

    # Incident Description
    description = st.text_area("Describe the incident:")

    # Location Input
    lat = st.number_input("Enter Latitude:", value=40.72)
    lon = st.number_input("Enter Longitude:", value=-74.00)
    user_location = (lat, lon)

    # Filters
    max_distance = st.slider("Select search radius (in km):", 1, 50, 10)
    availability = st.radio("Availability:", ["All", "Available", "Unavailable"])

    # Select responder count requirements
    police_needed = st.number_input("How many Policemen are needed?", min_value=0, value=1, step=1)
    firefighters_needed = st.number_input("How many Firefighters are needed?", min_value=0, value=1, step=1)
    volunteers_needed = st.number_input("How many Volunteers are needed?", min_value=0, value=1, step=1)
    total_responders = police_needed + firefighters_needed + volunteers_needed

    counts = {"Police": police_needed, "Firefighter": firefighters_needed, "Volunteer": volunteers_needed}

    # Load responders and filter them
    responders = load_responders()
    if availability != "All":
        responders = responders[responders["Availability"] == availability]

    nearby_responders = get_nearby_responders(user_location, responders, max_distance, counts)

    st.write("### Available Responders:")
    st.dataframe(nearby_responders)

    # Submit Button
    if st.button("🚨 Submit Incident Report"):
        if not incident_type or not description:
            st.error("Please provide all required details!", icon="⚠️")
            return

        incident_data = {
            "type": incident_type,
            "description": description,
            "lat": lat,
            "lon": lon,
            "responders_needed": total_responders
        }
        save_incident(incident_data)
        st.success("Incident report submitted successfully! 🚑 Authorities have been notified.", icon="✅")

report_incident()
