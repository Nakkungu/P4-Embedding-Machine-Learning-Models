import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

# Generate hashed passwords
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

# Define a function to render the sidebar
def render_sidebar():
    if st.session_state.get("authentication_status"):
        st.sidebar.write(f'Welcome, {st.session_state["name"]}!')
        # Add sidebar links here
        if st.sidebar.button("Home"):
            switch_page("Home")
        # Add logout button to the sidebar
        if st.session_state.logout_button:
            if st.sidebar.button("Logout"):
                authenticator.logout()
    else:
        st.sidebar.warning("Please log in to access the application.")

# Initialize logout button state
if "logout_button" not in st.session_state:
    st.session_state.logout_button = True

# Render the sidebar
render_sidebar()

# Render content based on authentication status
if st.session_state.get("authentication_status"):
    st.write(f'Welcome to the Churn App *{st.session_state["name"]}*')
    if st.button("Go to Home"):
        switch_page("Home")
elif st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect')
elif st.session_state.get("authentication_status") is None:
    st.warning('Please enter your username and password')
