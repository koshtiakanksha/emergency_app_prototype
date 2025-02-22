import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import sqlite3

# Database setup
DATABASE_FILE = "emergency_management.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    return conn, cursor


def load_responders():
    try:
        # Load responders from the database
        conn, cursor = get_db_connection()
        db_responders = pd.read_sql_query("SELECT name, role, availability, location, lat, lon FROM responders", conn)
        conn.close()
    except Exception as e:
        db_responders = pd.DataFrame()  # If database query fails, return empty DataFrame

    # Load responders from the CSV file (dummy data)
    try:
        csv_responders = pd.read_csv("responders.csv")
    except FileNotFoundError:
        csv_responders = pd.DataFrame()  # If file is missing, return empty DataFrame

    # Combine both datasets
    responders = pd.concat([db_responders, csv_responders], ignore_index=True)
    return responders


def load_incidents():
    conn, cursor = get_db_connection()
    df = pd.read_sql_query("SELECT type, description, lat, lon FROM incidents", conn)
    conn.close()
    return df


def display_map():
    responders = load_responders()
    incidents = load_incidents()

    map_center = [40.75, -74.00]
    m = folium.Map(location=map_center, zoom_start=12)

    role_styles = {
        "Police": {"color": "blue", "icon": "glyphicon-user"},
        "Firefighter": {"color": "red", "icon": "glyphicon-fire"},
        "Volunteer": {"color": "green", "icon": "glyphicon-heart"}
    }

    # Add responders to the map
    for _, row in responders.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"{row['Role']}: {row['Name']}",
            icon=folium.Icon(color=role_styles.get(row['Role'], {"color": "gray"})["color"],
                             icon=role_styles.get(row['Role'], {"icon": "info-sign"})["icon"])
        ).add_to(m)

    # Add incidents to the map
    for _, row in incidents.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"Incident: {row['type']}\nDescription: {row['description']}",
            icon=folium.Icon(color="black", icon="glyphicon-exclamation-sign")
        ).add_to(m)

    col1, col2 = st.columns([3, 1])
    with col1:
        st_folium(m, width=700, height=500)
    with col2:
        st.write("### Legend")
        st.markdown(
            """
            - <span style="color:blue">👮 **Police**</span> 
            - <span style="color:red">🔥 **Firefighter**</span> 
            - <span style="color:green">💚 **Volunteer**</span> 
            - ⚫ **Incidents** 
            """,
            unsafe_allow_html=True
        )


st.title("Live Map View 🗺️")
st.write("View real-time locations of responders and active incidents.")
display_map()
