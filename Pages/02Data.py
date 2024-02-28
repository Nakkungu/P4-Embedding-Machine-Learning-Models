import streamlit as st
import pandas as pd
import pyodbc
from dotenv import dotenv_values
from dotenv import load_dotenv
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page

if st.session_state.get("authentication_status"):
    if st.session_state["authentication_status"]:

        col1, col2, col3, col4, col5 = st.columns(5)

        if col1.button("Home"):
            switch_page("Home")

        if col2.button("data"):
            switch_page("data")

        if col3.button("dashboard"):
            switch_page("dashboard")

        if col4.button("predict"):
            switch_page("predict")

        if col5.button("history"):
            switch_page("history")

        # Get the directory of the current script
        current_dir = Path(__file__).resolve().parent

        # Load environment variables from .env file in the parent directory
        dotenv_path = current_dir.parent / '.env'
        load_dotenv(dotenv_path)

        # Load environment variables
        environment_variables = dotenv_values(dotenv_path)
        server = environment_variables.get("SERVER")
        username = environment_variables.get("USERNAME")
        password = environment_variables.get("PASSWORD")
        database = environment_variables.get("DATABASE")

        # Establish connection
        connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};MARS_Connection=yes;MinProtocolVersion=TLSv1.2;"
        connection = pyodbc.connect(connection_string)

        # Fetch data
        query = "Select * from dbo.LP2_Telco_churn_first_3000"
        df1 = pd.read_sql(query, connection)
        df2 = pd.read_csv("Data\LP2_Telco-churn-second-2000.csv")

        # Optional data cleaning (e.g., handling missing values)

        # Display headers and descriptions
        st.header("Telco Churn Data Exploration")
        st.subheader("First: 3000 rows from database")

        # Display DataFrame 1
        st.dataframe(df1.head())

        # Display DataFrame 2 with options
        st.subheader("Second: 2000 rows from CSV")
        show_full_df2 = st.checkbox("Show full DataFrame")
        if show_full_df2:
            st.dataframe(df2)
        else:
            st.dataframe(df2.head())

        # Implement interactive filtering, visualizations, etc.

        from joblib import dump, load
        # Load the cleaned data using joblib
        loaded_cleaned_training_data = load('packages\cleaned_training_data.joblib')
        # Display the loaded data using Streamlit
        st.header("Loaded Cleaned Training Data:")
        st.dataframe(loaded_cleaned_training_data)

        # Separate categorical and numerical columns
        categorical_columns = loaded_cleaned_training_data.select_dtypes(include=['object']).columns
        numerical_columns = loaded_cleaned_training_data.select_dtypes(exclude=['object']).columns

        # Sidebar selection for column type
        column_type = st.sidebar.radio("Select Column Type", ("Categorical", "Numerical"))

        if column_type == "Categorical":
            # Display categorical columns
            selected_column = st.selectbox("Select Categorical Column", categorical_columns)
            st.write(loaded_cleaned_training_data[selected_column].value_counts())

        else:
            # Display numerical columns
            selected_column = st.selectbox("Select Numerical Column", numerical_columns)
            st.write(loaded_cleaned_training_data[selected_column].describe())

        # Option to display the entire DataFrame
        show_full_df = st.checkbox("Show Full DataFrame")
        if show_full_df:
            st.write(loaded_cleaned_training_data)
    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')

st.header('Variable Description')
def load_variable_descriptions():
    descriptions = {}
    with open("Data/variable_descriptions.txt", "r") as file:
        for line_number, line in enumerate(file, start=1):
            parts = line.strip().split(" -- ", 1)
            if len(parts) == 2:
                variable, description = parts
                descriptions[variable.strip()] = description.strip()
            else:
                st.warning(f"Issue parsing line {line_number}: {line} - Expected format: 'Variable Name -- Description'")
    
    st.write(descriptions)  # Debug: Print loaded descriptions
    return descriptions

variable_descriptions = load_variable_descriptions()