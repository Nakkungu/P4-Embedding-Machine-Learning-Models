import streamlit as st
import pandas as pd
import sqlite3
import importlib.util
import os

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    """Creates the user table if it doesn't exist."""
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')

def add_userdata(username, password):
    """Adds a new user to the database."""
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    """Checks if the username and password match an existing user."""
    c.execute('SELECT * FROM usertable WHERE username = ? AND password = ?',(username, password))
    data = c.fetchall()
    return data

def load_page(module_name):
    """Loads a page dynamically using its module name."""
    spec = importlib.util.spec_from_file_location(module_name, os.path.join("Pages", f"{module_name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    """Simple login app with conditional page visibility."""
    st.title("Simple Login App")

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    logged_in = False  # Initialize login status

    if choice == "Home":
        if logged_in:
            st.subheader("Home content")  # Display home content if logged in
        else:
            st.info("Please log in to access this page.")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            result = login_user(username, password)
            if result:
                st.success("Logged In as {}".format(username))
                logged_in = True  # Set logged_in to True on successful login

                # Replace placeholders with actual dynamic page loading
                st.page_link("Pages/01Home.py", label="Home")
                # ... (similar links for other pages)

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("You have successfully created a new account")
            st.info("Go to Login Menu to login")

if __name__ == '__main__':
    main()
