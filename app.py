import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "views/home.py",
    title="Home",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "views/report_an_incident.py",
    title="Report an Incident",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "views/volunteer_and_respond.py",
    title="Volunteer and Respond",
    icon=":material/bar_chart:",
)
project_3_page = st.Page(
    "views/live_map_view.py",
    title="Live Map View",
    icon=":material/bar_chart:",
)
project_4_page = st.Page(
    "views/chatbot.py",
    title="Chat Bot Assistance",
    icon=":material/smart_toy:",
)
project_5_page = st.Page(
    "views/incident_logs_and_reports.py",
    title="Incident Logs and Reports",
    icon=":material/smart_toy:",
)



# --- NAVIGATION SETUP [WITHOUT SECTIONS]---
pg = st.navigation(pages = [about_page, project_1_page, project_2_page, project_3_page, project_4_page, project_5_page])


# --- SHARED ON ALL PAGES ---
st.sidebar.markdown("Akanksha Koshti")


# --- RUN NAVIGATION ---
pg.run()