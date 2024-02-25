import streamlit as st
from PIL import Image
st.set_page_config(
    page_title='My Awsome App',
    page_icon='🏠',
    layout='wide'
)
img = Image.open("Images\BGa.jpg")  
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

