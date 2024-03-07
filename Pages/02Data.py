import streamlit as st
from joblib import load
import pyodbc
import pandas as pd
from dotenv import dotenv_values 

st.set_page_config(
    page_title='Data',
    page_icon='📜',
    layout='wide'
)


# st.cache_resource(show_spinner='Connecting to database...')

# def initialize_connection():
#     connection = pyodbc.connect(
#         "DRIVER = {SQL Server};SERVER="
#         + st.secrets["SERVER"]
#         + ";DATABASE = "
#         + st.secrets["DATABASE"]
#         + ";UID="
#         + st.secrets["UID"]
#         + ";PWD="
#         + st.secrets["PWD"]

#     )
#     return connection


# conn = initialize_connection()

# #run a query to get data from database
# def query_database(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         rows = cur.fetchall()

#         df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])

#     return rows

# query = "Select * from dbo.LP2_Telco_churn_first_3000"
# query_database(query)




environment_variables = dotenv_values('.env')


# Get the values for the credentials you set in the '.env' file
server = environment_variables.get("SERVER")
username = environment_variables.get("USERNAME")
password = environment_variables.get("PASSWORD")
database = environment_variables.get("DATABASE")


#connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};MARS_Connection=yes;MinProtocolVersion=TLSv1.2;"

# Establish a connection to the database using the provided connection string.
connection = pyodbc.connect(connection_string)



def select_all_features():
     #load the first data
    query = "Select * from dbo.LP2_Telco_churn_first_3000"
    df = pd.read_sql(query, connection)

    return df

def select_numeric():
     #load the first data
    query = "Select * from dbo.LP2_Telco_churn_first_3000"
    df = pd.read_sql(query, connection)

    # Filter only numeric variables
    numeric_df = df.select_dtypes(include='number')

    return numeric_df

def select_categorical():
     #load the first data
    query = "Select * from dbo.LP2_Telco_churn_first_3000"
    df = pd.read_sql(query, connection)

    # Filter only categorical variables
    categorical_df = df.select_dtypes(include='object')

    return categorical_df

if __name__ == "__main__":
    select_all_features()

# Sidebar to select option
    option = st.sidebar.selectbox("Select data type", ["All Data", "Numeric Data", "Categorical Data"])

    # Display corresponding data
    if option == "All Data":
        df = select_all_features()
        st.title("All Data")
    elif option == "Numeric Data":
        df = select_numeric()
        st.title("Numeric Data")
    elif option == "Categorical Data":
        df = select_categorical()
        st.title("Categorical Data")

    # Display DataFrame
    st.write(df)
   

