import streamlit as st

st.set_page_config(
    page_title='Predict',
    page_icon='🔮',
    layout='wide'
)
# #['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
#        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
#        'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
#        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
#        'MonthlyCharges', 'TotalCharges', 'Churn']

def form1():

    col1, col2 = st.columns(2)

    with st.form('Insert-Variable-Values'):
        with col1:
            st.subheader('Numerical Variables')
            st.number_input('Enter Total Charge')
            st.number_input('Enter Monthly Charge')
            st.number_input('Enter Tenure')
        with col2:
            st.subheader('Categorical Variables')
            st.selectbox('Enter gender', options=['Female', 'Male'])
            st.selectbox('Enter Senior Citizenship status', options=['Yes', 'No'])
            st.selectbox('Enter Dependants status', options=['Yes', 'No'])
            st.selectbox('Enter Phone Service status', options=['Yes', 'No'])
            st.selectbox('Enter Multiple Lines status', options=['None', 'No', 'Yes', 'No phone service'])
            st.selectbox('Enter InternetService status', options=['DSL', 'Fiber optic', 'No'])
            st.selectbox('Enter Online Security status', options=['No', 'Yes',' None', 'No internet service'])
            st.selectbox('Enter Online BackUp status', options=['No', 'Yes',' None', 'No internet service'])
            st.selectbox('Enter Device Protection status', options=['No', 'Yes',' None', 'No internet service'])
            st.selectbox('Enter Tech Support status', options=['No', 'Yes',' None', 'No internet service'])
            st.selectbox('Enter Streming TV status', options=['No', 'Yes',' None', 'No internet service'])
            st.selectbox('Enter Streaming Movies status', options=['No', 'Yes',' None', 'No internet service'])
            st.selectbox('Enter Contract status', options=['Month-to-month', 'One year', 'Two year'])
            st.selectbox('Enter Paperless billing status', options=['Yes', 'No'])
            st.selectbox('Enter Payment Method', options=['Electronic check', 'Mailed check', 'Bank transfer(automatic)','Credit Card(automatic)'])



        st.form_submit_button('Submit')


form1()
