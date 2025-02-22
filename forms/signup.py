import re
import streamlit as st
import sqlite3


# Function to establish a new database connection per thread
def get_db_connection():
    conn = sqlite3.connect("local_users.db", check_same_thread=False)
    return conn, conn.cursor()


def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


def set_logged_in(name):
    st.session_state["logged_in"] = True
    st.session_state["user_name"] = name
    st.rerun()


def sign_up():
    conn, cursor = get_db_connection()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()

    st.title("Sign Up")
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        if not name or not email or not password:
            st.error("All fields are required!", icon="⚠️")
            return
        if not is_valid_email(email):
            st.error("Invalid email format!", icon="📧")
            return

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            st.success("Account created successfully! Redirecting...", icon="✅")
            set_logged_in(name)
        except sqlite3.IntegrityError:
            st.error("This email is already registered. Please use another email.", icon="🚫")
        finally:
            conn.close()


def log_in():
    conn, cursor = get_db_connection()
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Log In")

    if submit_button:
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        if user:
            st.success(f"Welcome back, {user[1]}! Redirecting...", icon="🎉")
            set_logged_in(user[1])
        else:
            st.error("Invalid email or password. Please try again.", icon="🚨")

    conn.close()


def dashboard():
    st.title("Welcome to the Emergency Management System")
    st.write("Here are the features you can use:")
    st.markdown("""
    - **📍 Report an Incident**: Log emergency cases in real-time.
    - **🚑 View and Request Responders**: Check available emergency responders.
    - **🗺️ Live Map View**: Monitor incidents on an interactive map.
    - **💬 Chatbot Assistance**: Get AI-driven help for emergencies.
    """)


if "logged_in" in st.session_state and st.session_state["logged_in"]:
    dashboard()
else:
    sign_up()
