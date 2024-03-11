import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

# Generate hashed passwords (replace with your actual password hashing logic)
hashed_passwords = stauth.Hasher(['your_password1', 'your_password2']).generate()

import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, message = authenticator.login(fields=['username', 'password'])


if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Enjoy Exploring the App')
    

elif authentication_status == False or authentication_status is None:
    st.write('Use this login')
    st.write('Username: rbriggs')
    st.write('Password: rem')
    
    if authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')