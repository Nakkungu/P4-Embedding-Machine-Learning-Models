import streamlit as st
import joblib
import pandas as pd
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
        # st.set_page_config(
        #     page_title='Predict',
        #     page_icon='🔮',
        #     layout='wide'
        # )
        # #['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        #        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
        #        'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
        #        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
        #        'MonthlyCharges', 'TotalCharges', 'Churn']
        st.cache_resource(show_spinner ='Loading')

        def load_model1():
            pipeline = joblib.load('Models\decision_tree_model.joblib')
            return pipeline


        st.cache_resource(show_spinner ='Loading')
        def load_model2():
            pipeline = joblib.load('Models\logistic_regression_model.joblib')
            return pipeline

        st.cache_resource()

        def select_model():
            encoder = joblib.load('Models\label_encoder.joblib')

            st.selectbox('Select a model', options=['Decision Tree', 'Random Forest'],
            key = 'selected_model')

            if st.session_state['selected_model'] == 'Random Forest':
                pipeline=load_model2()

            else:
                pipeline = load_model1()

            return pipeline, encoder

        def make_prediction(pipeline, encoder):

            Total_Charge = st.session_state['Total_Charge']
            Monthly_Charge = st.session_state['Monthly_Charge']
            Tenure = st.session_state['Tenure']
            gender = st.session_state['gender']
            Senior_Citizenship = st.session_state['Senior_Citizenship']
            Dependants = st.session_state['Dependants']
            Phone_Service = st.session_state['Phone_Service']
            Multiple_Lines = st.session_state['Multiple_Lines']
            InternetService = st.session_state['InternetService']
            Online_Security = st.session_state['Online_Security']
            Online_BackUp = st.session_state['Online_BackUp']
            Device_Protection = st.session_state['Device_Protection']
            Tech_Support = st.session_state['Tech_Support']
            Streaming_TV= st.session_state['Streming_TV']
            Streaming_Movies= st.session_state['Streaming_Movies']
            Contract = st.session_state['Contract']
            Paperless_billing = st.session_state['Paperless_billing']
            Payment_Method= st.session_state['Payment_Method']
            gender = st.session_state['gender']
            

            columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
            'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
            'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
            'MonthlyCharges', 'TotalCharges']
            
            data = [[Total_Charge, Monthly_Charge,Tenure, gender,Senior_Citizenship,  Dependants, Phone_Service,
                    Multiple_Lines,InternetService,Online_Security, Online_BackUp, Device_Protection,Tech_Support,
                        Streaming_TV, Streaming_Movies, Contract,Paperless_billing,  Payment_Method ]]

            df = pd.DataFrame(data,columns=columns)

            pred = pipeline.predict(df)

            st.session_state['pred'] = pred

            return pred
        def form1():
            with st.form('Insert-Variable-Values'):
            
                # pipeline, encoder = select_model()
                
                col1, col2, col3 = st.columns(3)

            
                with col1:
                    st.subheader('Numerical Variables')
                    st.number_input('Enter Total Charge', key = 'Total_Charge')
                    st.number_input('Enter Monthly Charge', key = 'Monthly_Charge')
                    st.number_input('Enter Tenure',key ='Tenure')
                with col2:
                    st.subheader('Categorical Variables')
                    st.selectbox('Enter gender', options=['Female', 'Male'], key='gender')
                    st.selectbox('Enter Senior Citizenship status', options=['Yes', 'No'], key= 'Senior_Citizenship')
                    st.selectbox('Enter Dependants status', options=['Yes', 'No'], key = 'Dependants')
                    st.selectbox('Enter Phone Service status', options=['Yes', 'No'], key ='Phone_Service')
                    st.selectbox('Enter Multiple Lines status', options=['None', 'No', 'Yes', 'No phone service'], key='Multiple_Lines' )
                    st.selectbox('Enter InternetService status', options=['DSL', 'Fiber optic', 'No'], key ='InternetService')
                    st.selectbox('Enter Online Security status', options=['No', 'Yes',' None', 'No internet service'], key ='Online_Security')
                    st.selectbox('Enter Online BackUp status', options=['No', 'Yes',' None', 'No internet service'], key ='Online_BackUp')

                with col3:
                    st.subheader('Categorical Variables')
                    st.selectbox('Enter Device Protection status', options=['No', 'Yes',' None', 'No internet service'], key = 'Device_Protection')
                    st.selectbox('Enter Tech Support status', options=['No', 'Yes',' None', 'No internet service'], key ='Tech_Support')
                    st.selectbox('Enter Streaming TV status', options=['No', 'Yes',' None', 'No internet service'], key ='Streaming_TV')
                    st.selectbox('Enter Streaming Movies status', options=['No', 'Yes',' None', 'No internet service'], key ='Streaming_Movies')
                    st.selectbox('Enter Contract status', options=['Month-to-month', 'One year', 'Two year'], key ='Contract')
                    st.selectbox('Enter Paperless billing status', options=['Yes', 'No'], key ='Paperless_billing')
                    st.selectbox('Enter Payment Method', options=['Electronic check', 'Mailed check', 'Bank transfer(automatic)','Credit Card(automatic)'], key ='Payment_Method')
            # st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))
                    
                st.form_submit_button('Submit')


            # select_model()
            
        if __name__ == '__main__':
            st.title('Prediction')
            form1()
            
            
                

            # final_pred = st.session_state['pred']
            # st.write(final_pred)
            st.write(st.session_state)
    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')  