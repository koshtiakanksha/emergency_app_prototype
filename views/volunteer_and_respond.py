import streamlit as st
import sqlite3
import pandas as pd
import geopy.distance
import sqlite3

# Database setup
DATABASE_FILE = "responders.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            role TEXT,
            availability TEXT,
            location TEXT,
            lat REAL,
            lon REAL
        )
    """)
    conn.commit()
    return conn, cursor


def save_responder(responder_data):
    conn, cursor = get_db_connection()
    cursor.execute("""
        INSERT INTO responders (name, role, availability, location, lat, lon)
        VALUES (?, ?, ?, ?, ?, ?)""",
                   (responder_data["Name"], responder_data["Role"], "Available", responder_data["Location"],
                    responder_data["lat"], responder_data["lon"])
                   )
    conn.commit()
    conn.close()


def register_responder():
    st.title("Become a Responder")
    st.write("### Make a difference today! 🚑")
    st.write(
        "Join our network of dedicated responders—whether you're a **Police Officer, Firefighter, or Volunteer**,"
        "your role is crucial in saving lives and assisting communities in times of need.Sign up now and be a hero!"
    )

    with st.form("responder_signup_form"):
        name = st.text_input("Full Name")
        role = st.selectbox("Select Your Role", ["Police", "Firefighter", "Volunteer"])
        location = st.text_input("Enter Your Location (e.g., North, South, East, West, Central)")
        lat = st.number_input("Enter Your Latitude:", value=40.72)
        lon = st.number_input("Enter Your Longitude:", value=-74.00)
        submit_button = st.form_submit_button("Sign Up as Responder")

    if submit_button:
        if not name or not role or not location:
            st.error("All fields are required!", icon="⚠️")
            return

        responder_data = {
            "Name": name,
            "Role": role,
            "Location": location,
            "lat": lat,
            "lon": lon
        }
        save_responder(responder_data)
        st.success(f"Welcome, {name}! You are now registered as a {role}.", icon="✅")
        st.session_state["responder"] = True
        st.session_state["responder_name"] = name
        st.session_state["responder_role"] = role
        st.session_state["responder_location"] = location
        st.rerun()


def view_incidents():
    st.title("View & Respond to Incidents")
    st.write("### Active Emergency Incidents")

    incidents = pd.DataFrame([
        {"Incident_ID": 1, "Type": "Fire", "Location": "Central", "lat": 40.75, "lon": -74.05},
        {"Incident_ID": 2, "Type": "Medical Emergency", "Location": "North", "lat": 40.71, "lon": -74.01}
    ])
    st.dataframe(incidents)

    selected_incident = st.selectbox("Select an incident to respond:", incidents["Incident_ID"].tolist())

    if st.button("🚑 Respond to Incident"):
        st.success("You have chosen to respond to the incident! Authorities have been notified.", icon="🚨")

    st.write("### Respond to Direct Requests")
    if st.button("✅ Accept Request"):
        st.success("You have accepted the response request!", icon="✅")
    if st.button("❌ Deny Request"):
        st.warning("You have denied the response request.", icon="⚠️")


if "logged_in" in st.session_state and st.session_state["logged_in"]:
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM responders WHERE name = ?", (st.session_state["user_name"],))
    existing_responder = cursor.fetchone()
    conn.close()

    if existing_responder:
        view_incidents()
else:
    register_responder()


