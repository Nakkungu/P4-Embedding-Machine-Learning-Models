import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title='My Awesome App',
    page_icon='🏠',
    layout='wide'
)

# Check authentication status
if st.session_state.get("authentication_status"):
    if st.session_state["authentication_status"]:
        st.write(f'Welcome to the Churn App *{st.session_state["name"]}*')

        # Navigation buttons
        col1, col2, col3, col4, col5 = st.columns(5)

        if col1.button("Home"):
            switch_page("Home")

        if col2.button("Data"):
            switch_page("data")

        if col3.button("Dashboard"):
            switch_page("dashboard")

        if col4.button("Predict"):
            switch_page("predict")

        if col5.button("History"):
            switch_page("history")

        # Header image and title
        img = Image.open("Images/BGa.jpg")
        st.image(img, width=None, use_column_width=True)  # Stretch image across the page
        st.title("Churn Prediction App")

        # Description
        st.write("""
        This app is built to predict customer churn using machine learning models trained on existing data. 
        Use the navigation buttons above to explore different sections of the app.
        """)

        # Columns for explanation and links
        col1, col2, col3 = st.columns(3)

        # Column 1: Explanation
        with col1:
            st.subheader("How to Use:")
            st.write("1. **Data**: Explore and analyze the dataset.")
            st.write("2. **Dashboard**: Visualize key metrics and insights.")
            st.write("3. **Predict**: Make predictions on customer attrition.")
            st.write("4. **History**: View past predictions and results.")

            st.write("You can click on the buttons above to navigate to each section.")

        # Column 2: Links
        with col2:
            st.subheader("Get Help:")
            st.write("If you need assistance, check out these resources:")
            st.markdown("[User Guide](https://example.com/user-guide): Detailed instructions on using the app.")
            st.markdown("[FAQs](https://example.com/faqs): Answers to common questions.")

        # Column 3: Source Code and Social Links
        with col3:
            st.subheader("Get Involved:")
            st.write("Connect with us and contribute to the project:")
            st.markdown("[GitHub](https://github.com/Nakkungu/P4-Embedding-Machine-Learning-Models): View and contribute to the source code.")
            st.markdown("[LinkedIn](https://www.linkedin.com/in/angella-nakkungu/): Connect with the developer.")
            st.markdown("[Medium](https://medium.com/@angellanakkungu): Read articles and updates.")

    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')
