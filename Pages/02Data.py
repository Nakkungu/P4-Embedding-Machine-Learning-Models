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


if st.session_state.get("authentication_status"):
    if st.session_state["authentication_status"]:
        st.write(f'Welcome to the Churn App *{st.session_state["name"]}*')


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
        # Description of the columns
        with st.expander("Column Descriptions", expanded=True):
            st.info("""
            - **Gender**: Whether the customer is a male or a female
            - **SeniorCitizen**: Whether a customer is a senior citizen or not
            - **Partner**: Whether the customer has a partner or not (Yes, No)
            - **Dependents**: Whether the customer has dependents or not (Yes, No)
            - **Tenure**: Number of months the customer has stayed with the company
            - **PhoneService**: Whether the customer has a phone service or not (Yes, No)
            - **MultipleLines**: Whether the customer has multiple lines or not
            - **InternetService**: Customer's internet service provider (DSL, Fiber Optic, No)
            - **OnlineSecurity**: Whether the customer has online security or not (Yes, No, No Internet)
            - **OnlineBackup**: Whether the customer has online backup or not (Yes, No, No Internet)
            - **DeviceProtection**: Whether the customer has device protection or not (Yes, No, No internet service)
            - **TechSupport**: Whether the customer has tech support or not (Yes, No, No internet)
            - **StreamingTV**: Whether the customer has streaming TV or not (Yes, No, No internet service)
            - **StreamingMovies**: Whether the customer has streaming movies or not (Yes, No, No Internet service)
            - **Contract**: The contract term of the customer (Month-to-Month, One year, Two year)
            - **PaperlessBilling**: Whether the customer has paperless billing or not (Yes, No)
            - **PaymentMethod**: The customer's payment method (Electronic check, mailed check, Bank transfer(automatic), Credit card(automatic))
            - **MonthlyCharges**: The amount charged to the customer monthly
            - **TotalCharges**: The total amount charged to the customer
            - **Churn**: Whether the customer churned or not (Yes or No)
            """)

    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')


   

