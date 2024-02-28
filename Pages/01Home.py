import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
# Check authentication status
if st.session_state.get("authentication_status"):
    if st.session_state["authentication_status"]:
        st.write(f'Welcome to the Churn App *{st.session_state["name"]}*')
        # Content of the specific page goes here

        # st.set_page_config(
        #     page_title='My Awesome App',
        #     page_icon='🏠',
        #     layout='wide'
        # )


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

        img = Image.open("Images/BGa.jpg")
        st.image(img, width=None, use_column_width=True)  # Stretch image across the page

        st.title("Attrition Prediction App", anchor="home")  # Use "home" for navigation link
        st.subheader("This App is built to predict customer attrition using models built from existing data")

        # Layout with two columns
        col1, col2 = st.columns(2)

        # Column 1: Title, subheader, description
        with col1:
            st.title("My Awesome App")
            st.subheader("Predict the future with incredible accuracy!")
            st.markdown("""
            This amazing app utilizes cutting-edge Machine Learning to help you predict things you thought were impossible. Try it out and be amazed!
            """)

        # Column 2: Links and source code
        with col2:
            st.write("Get Involved:")
            st.markdown("[GitHub](https://github.com/Nakkungu)")
            st.markdown("[LinkedIn](https://www.linkedin.com/in/angella-nakkungu/)")
            st.markdown("[Medium](https://medium.com/@angellanakkungu)")
    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')