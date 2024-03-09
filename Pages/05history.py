import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd

st.set_page_config(
    page_title='History',
    page_icon='🔙',
    layout='wide'
)

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

        def show_historic_predictions():
            csv_path = "./ddata/history.csv"
            df = pd.read_csv(csv_path)

            return df

        if __name__ == "__main__":
          df = show_historic_predictions()  
          st.dataframe(df)
        
                

    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')  