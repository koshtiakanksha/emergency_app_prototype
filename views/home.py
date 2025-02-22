import streamlit as st
from forms.signup import sign_up, log_in

@st.dialog("Sign up")
def show_signup_form():
    sign_up()


@st.dialog("Log in")
def show_login_form():
    log_in()

# --- HERO SECTION ---
# banner = "https://media.giphy.com/media/3o6ZtpYw4gBrbmh6Kc/giphy.gif"
# st.image(banner, use_container_width=True)

st.title('Emergency Management Tool')
st.subheader('Real-time coordination and responder tracking')
st.write(
    "This platform helps streamline emergency response by enabling quick incident logging,"
    " geolocation tracking, and effective communication with responders."
)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔑 Sign Up"):
        show_signup_form()
with col2:
    if st.button("🔓 Login"):
        show_login_form()

